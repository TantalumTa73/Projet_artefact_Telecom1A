# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, Response
import controller
import time
import datetime
import module_camera
import os
import moteur
import requests

# Moteurs 

global vitesse
vitesse = 0

url = "https://comment.requestcatcher.com/"

last_update_time = time.time()
users_connected = dict() 
cam = None 

c = controller.Controller()
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
	except Exception as e:
		error_message = str(e)
		print("Moteur ne marchent pas")
		print(error_message)
		return Response(status=500)
	return render_template("page.html")	

@app.route('/change-speed', methods=['POST'])
def change_speed():
	global vitesse
	vitesse = request.form.get('speed')
	print(f"Setting speed to {vitesse}")
	return render_template("page.html")	

@app.route('/forward-press', methods=['POST'])
def forward():
	global vitesse
	moteur.avance_corrige("left", 1, vitesse)
	return render_template("page.html")	

@app.route('/backward-press', methods=['POST'])
def backward():
	global vitesse
	moteur.avance_corrige("left", 1, -vitesse)
	return render_template("page.html")	

@app.route('/right-press', methods=['POST'])
def right():
	global vitesse
	moteur.avance_corrige("left", -1, vitesse)
	return render_template("page.html")	

@app.route('/left-press', methods=['POST'])
def left():
	global vitesse
	moteur.avance_corrige("right", -1, vitesse)
	return render_template("page.html")	

@app.route('/button-release', methods=['POST'])
def test_button_release():
	moteur.avance_corrige("left", 1, 0)
	return render_template("page.html")	


@app.route('/update')
def update():
	global last_update_time, users_connected, cam
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

	# Connection de la camera
	if cam is None:
		cam = module_camera.connect()
	aruco_detected = module_camera.check_aruco(cam)
	connexion = module_camera.check_camera_status(cam,verbose=True)

	###### Code qui s'exécute toute les secondes #######
	if now - last_update_time >= 0.9:
		# Envoi vers l'api 
		r = requests.post(url)

		if r.status_code == 200: 
			print("Data sent to server")



		# Saving image
		print("Attempt to save image")
		image = module_camera.get_image(cam)
		module_camera.save_image(image)

		last_update_time = now
	#####################################################

		
	# Contenu renvoier
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

