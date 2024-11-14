# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
import controller
import time
import datetime
import module_camera
import os
import moteur

# Moteurs 

last_update_time = time.time()
users_connected = dict() 

c = controller.Controller()
c.standby()

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__, static_url_path='/static/')

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

def get_index(elm,tab):
	for i in range(len(tab)):
		if elm == tab[i]:
			return i
	return None

@app.route('/', methods=['GET','POST'])
def page():
	global c 

	if request.method == 'POST':
		if request.form['button'] == '1':
			c.set_raw_motor_speed(100,100)
		if request.form['button'] == '2':
			c.standby()

	# If the method is GET,render the HTML page to the user
	#if request.method == 'GET':
	#return 

	return render_template("page.html")	

@app.route('/slider', methods=['POST'])
def slider():
	global c 

	if request.method == 'POST':
		number = int(request.form['valeur'])
		c.set_raw_motor_speed(-number,number)
	return render_template("page.html")	

@app.route('/test_calibrage', methods=['POST'])
def test_calibrage():
	moteur_princ = request.form.get('text')
	ratio = request.form.get('num2')

	try:
		moteur.avance_corrige(moteur_princ, ratio, 100)
		print("C bien")
	except Exception as e:
		error_message = str(e)
		print("C pas bien")
		print(error_message)
		return render_template('page.html', error=error_message)

@app.route('/forward-press', methods=['POST'])
def forward():
	moteur.avance_corrige("left", 1, 100)

@app.route('/backward-press', methods=['POST'])
def backward():
	moteur.avance_corrige("left", 1, -100)

@app.route('/right-press', methods=['POST'])
def right():
	moteur.avance_corrige("left", -1, 100)

@app.route('/left-press', methods=['POST'])
def left():
	moteur.avance_corrige("right", -1, 100)

@app.route('/button-release', methods=['POST'])
def test_button_release():
	moteur.avance_corrige("left", 1, 0)


@app.route('/update')
def update():
	global last_update_time, users_connected
	"""send current content"""

	now = time.time()
	current_user = request.remote_addr

	# Determination du nombre d'utilisateur connecte 
	if current_user not in users_connected.keys():
		users_connected[current_user] = now

	to_remove = []
	for user in users_connected.keys():
		if now - users_connected[user] > 2:
			to_remove.append(user)

	for user in to_remove:
		del users_connected[user]



	module_camera.save_image()
	connexion = module_camera.check_connexion()
	print("connexion camera : ", connexion)
	if connexion :
		print("try to save the image")
		module_camera.save_image()

	aruco_detected = module_camera.check_aruco()
	updated_content=f"""
<p>Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} </p>
<p>connexion camera : {connexion}</p>
<p>aruco détecté: {aruco_detected}</p>
<p>aruco détecté: {aruco_detected}</p>
<p>nombre d'utilisateurs connectés {len(users_connected)}</p>
"""

	return updated_content




# main driver function
if __name__ == '__main__':
	# run() method of Flask class runs the application 
	# on the local development server.
	#app.run()
	app.run(debug=True,host="0.0.0.0")

