# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, Response
from position_robot import Position_robot
import controller
import time
import datetime
import module_camera
import os
import moteur
import requests
import analyse_image
import main

# Moteurs 

global vitesse
global left_speed
global right_speed
vitesse = 0
left_speed = 0
right_speed = 0

url = "http://proj103.r2.enst.fr/"#"https://comment.requestcatcher.com/"




current_pos = Position_robot((25,25),(0,1))

last_distance = ""
last_update_time = time.time()
users_connected = dict() 
cam = None 
image_view = True

c = controller.Controller()
c.standby()

def send_position(x,y):
	r = requests.post(url+f"/api/pos?x={x}&y={y}")

	if r.status_code != 200: 
		print(f"Failed to send data to server {r.status_code}")

def get_status():
	r = requests.get(url+"/api/status")
	if r.status_code != 200: 
		print(f"Failed to retrieve data from server {r.status_code}")
	else:
		return r.json()

def found_flag(marquer_id,col,row):
	r = requests.post(url+f"/api/marker?id={marquer_id}&col={col}&row={row}")

	if r.status_code != 200: 
		print(f"Failed to send data to server {r.status_code}")

def case_to_pos(case):
	"""revoie la position (x,y) en centimètre du milieu de la case (i,j)"""
	i,j = case 
	return (25+i*50, -25+j*50)

def pos_to_case(pos):
	"""renvoie la case (i,j) à paritr de la pos (x,y)  en centimètres"""
	x,y = pos 
	return (x//50, (25+y)//50)

def case_to_string(case):
	"""renvoie le string lettre+chiffre à partir de la case (i,j)"""
	i,j = case
	if not (0<=i<7 or 0<=j<7):
		return "Hors du terrain"
		print("Hors du terrain")
	string = "GFEDCBA"[j]
	return (string,str(i+1))

def string_to_case(case):
	"""renvoie la case (i,j) correspondant au string
	None si le format est incorrect"""
	j = "GFEDCBA".find(case[0])
	if j==-1:
		"gfedcba".find(case[0])
	return (int(case[1])-1,j)


# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__, static_url_path='/static/')

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

@app.route('/', methods=['GET','POST'])
def page():
	return render_template("page.html")	

@app.route('/init_position', methods=['POST'])
def init_position():
	global current_pos
	case_x = request.form.get('x')
	case_y = request.form.get('y')
	print(case_x,case_y)

	current_pos.set_pos(*case_to_pos(string_to_case((case_x,case_y))))

	send_position(*current_pos.get_pos())
	return render_template("page.html")	


@app.route('/go_to', methods=['POST'])
def go_to():
	global current_pos
	case_x = request.form.get('x')
	case_y = request.form.get('y')

	target_x, target_y = case_to_pos(string_to_case((case_x,case_y)))
	main.aller_case(target_x, target_y, position_robot)

	return render_template("page.html")	

@app.route('/change-speed', methods=['POST'])
def change_speed():
	global vitesse
	vitesse = int(request.form.get('speed'))
	print(f"Setting speed to {vitesse}")
	return render_template("page.html")	

@app.route('/forward-press', methods=['POST'])
def forward():
	global vitesse, left_speed, right_speed
	if left_speed < vitesse and right_speed < vitesse:
		left_speed += vitesse
		right_speed += vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	

@app.route('/downward-press', methods=['POST'])
def backward():
	global vitesse, left_speed, right_speed
	if left_speed > - vitesse and right_speed > -vitesse:
		left_speed -= vitesse
		right_speed -= vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	

@app.route('/right-press', methods=['POST'])
def right():
	global vitesse, left_speed, right_speed
	if left_speed == 0 and right_speed == 0:
		right_speed -= vitesse
		left_speed += vitesse
	elif left_speed <= vitesse and right_speed > 0:
		left_speed += vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	

@app.route('/left-press', methods=['POST'])
def left():
	global vitesse, left_speed, right_speed
	if left_speed == 0 and right_speed == 0:
		right_speed += vitesse
		left_speed -= vitesse
	elif right_speed <= vitesse	and left_speed > 0:
		right_speed += vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	

@app.route('/forward-release', methods=['POST'])
def forward_rel():
	global vitesse, left_speed, right_speed
	left_speed -= vitesse
	right_speed -= vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	

@app.route('/downward-release', methods=['POST'])
def backward_rel():
	global vitesse, left_speed, right_speed
	left_speed += vitesse
	right_speed += vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	

@app.route('/right-release', methods=['POST'])
def right_rel():
	global vitesse, left_speed, right_speed
	print(left_speed, right_speed)
	if left_speed == -right_speed:
		right_speed += vitesse
		left_speed -= vitesse
	else:
		left_speed -= vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	

@app.route('/left-release', methods=['POST'])
def left_rel():
	global vitesse, left_speed, right_speed
	print(left_speed, right_speed)
	if left_speed == - right_speed:
		right_speed -= vitesse
		left_speed += vitesse
	else:
		right_speed -= vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	


@app.route('/toggle-image-view', methods=['POST'])
def toggle_image_view():
	global image_view
	image_view = not image_view
	return render_template("page.html")	



@app.route('/update')
def update():
	global last_update_time, users_connected, cam, last_distance, current_pos
	"""send current content"""

	now = time.time()
	current_user = request.remote_addr

	updated_content = f"<p>Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} </p>"


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
	if image_view:
		if cam is None:
			cam = module_camera.connect()
		connexion = module_camera.check_camera_status(cam,verbose=True)
		updated_content+=f"<p>Connexion camera : {connexion}</p>"

	###### Code qui s'exécute toute les secondes #######
	if now - last_update_time >= 0.9:
		# Envoi vers l'api 
		#send_position(x, y)
		#status = get_status()
		#found_flag(marquer_id, col, row)



		# Saving image
		if image_view:
			image, result = module_camera.get_image(cam)
			if result:
				module_camera.save_image(image)
				last_distance = f"{analyse_image.detect_aruco_markers(image)}"
			else:
				print("Image did not save")

		last_update_time = now
	#####################################################

		
	# Contenu renvoier
	updated_content+=f"<p>En mouvement: {current_pos.is_moving()}</p>"
	updated_content+=f"<p>État des moteurs {controller.get_motor_speed()}</p>"
	updated_content+=f"<p>Vitesse actuelle: {vitesse}</p>"
	updated_content+=f"<p>Position actuelle (cm) x:{current_pos.get_pos()[0]} y:{current_pos.get_pos()[1]} angle:{current_pos.get_angle_orientation()}</p>"
	case_x,case_y= pos_to_case(current_pos.get_pos())
	str_x, str_y = case_to_string((case_x,case_y))
	updated_content+=f"<p>Position actuelle (case) {str_x}{str_y}</p>"
	updated_content+=f"<p>Nombre d'utilisateurs connectés {len(users_connected)}</p>"
	updated_content+=f"<p>Analyse aruco {last_distance}</p>"
	updated_content+="<p>Utilisateurs connectés</p>"
	updated_content+="<ul>"
	for user in sorted(users_connected):
		updated_content += f"<li>{user}</li>"
	updated_content += "</ul>"

	return updated_content




# main driver function
if __name__ == '__main__':
	# run() method of Flask class runs the application 
	# on the local development server.
	#app.run()
	app.run(debug=True,host="0.0.0.0")

