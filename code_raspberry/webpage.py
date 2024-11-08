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
users_connected = 0
nb_request_per_sec = 0
last_five_nb = [0,0,0,0,0]

c = controller.Controller()
c.set_motor_shutdown_timeout(2)
c.standby()

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__, static_url_path='/static/')

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.


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

	return render_template("page.html")

@app.route('/update')
def update():
	global last_update_time, nb_request_per_sec, users_connected
	"""send current content"""

	now = time.time()

	# Determination du nombre d'utilisateur connecte 
	if abs(now - last_update_time) <= 1.2:
		nb_request_per_sec+=1
	else:
		last_update_time = now
		last_five_nb.pop(0)
		last_five_nb.append(nb_request_per_sec)
		users_connected = sum(last_five_nb)//5
		nb_request_per_sec = 0

	connexion = module_camera.check_connexion()
	aruco_detected = module_camera.check_aruco()
	if connexion :
		module_camera.save_image()

	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+f"connexion camera : {connexion}; aruco détecté: {aruco_detected}; nombre d'utilisateurs connectés {users_connected}"




# main driver function
if __name__ == '__main__':
	# run() method of Flask class runs the application 
	# on the local development server.
	#app.run()
	app.run(debug=True,host="0.0.0.0")

