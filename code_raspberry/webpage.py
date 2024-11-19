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
import analyse_image

# Moteurs 

global vitesse
vitesse = 0

url = "http://proj103.r2.enst.fr/"#"https://comment.requestcatcher.com/"

current_x = 0
current_y = 0
current_angle = 0

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
	return (25+i*50, 25+j*50)

def pos_to_case(pos):
	"""renvoie la case (i,j) à paritr de la pos (x,y)  en centimètres"""
	x,y = pos 
	return ((x-25)//50, (y-25)//50)

def case_to_string(case):
	"""renvoie le string lettre+chiffre à partir de la case (i,j)"""
	i,j = case 
	if i<0 or i>3 or j<0 or j>6:
		print("Hors du terrain")
	string = "GFEDCBA"[j]
	return (string,str(i+1))

def string_to_case(case):
	"""renvoie la case (i,j) correspondant au string
	None si le format est incorrect"""
	j = "GFEDCBA".find(case[0])
	if j==-1:
		"gfedcba".find(case[0])
	return (j, int(case[1]))
	
	


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
	global current_x, current_y
	case_x = request.form.get('x')
	case_y = request.form.get('y')
	print(case_x,case_y)

	current_x, current_y = case_to_pos(string_to_case((case_x,case_y)))

	return render_template("page.html")	


@app.route('/go_to', methods=['POST'])
def go_to():
	global current_x, current_y
	case_x = request.form.get('x')
	case_y = request.form.get('y')

	x, y = case_to_pos(string_to_case((case_x,case_y)))

	return render_template("page.html")	

@app.route('/test_calibrage', methods=['POST'])
def test_calibrage():
	moteur_princ = request.form.get('text')
	ratio = request.form.get('ratio')

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
	vitesse = int(request.form.get('speed'))
	print(f"Setting speed to {vitesse}")
	return render_template("page.html")	

@app.route('/avance-test', methods=['POST'])
def avance_test():
	moteur.avance_test()

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

@app.route('/toggle-image-view', methods=['POST'])
def toggle_image_view():
	global image_view
	image_view = not image_view
	return render_template("page.html")	



@app.route('/update')
def update():
	global last_update_time, users_connected, cam, last_distance, current_x, current_y, current_angle
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
	updated_content+=f"<p>Vitesse actuelle: {vitesse}</p>"
	updated_content+=f"<p>Position actuelle (cm) x:{current_x} y:{current_y} angle:{current_angle}</p>"
	str_x, str_y = case_to_string(pos_to_case((current_x,current_y)))
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

