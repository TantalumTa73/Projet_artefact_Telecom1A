# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, Response
import logging 
from position_robot import Position_robot
import position_from_arucos
import controller
import time
import datetime
import module_camera
import os
import moteur
import requests
import analyse_image
import analyser_drapeau
import main
import vecteur_2d


host_robot = 4
os.environ["ARTEFACT_SERVER_HOST"] = f"robotpi-6{host_robot}.enst.fr"
import strat
from strat.client.utils import receive_instructions, Instruction, send_flag
from strat.common.grid import Cell, Direction, Flag
from strat.common.protocol import MsgType

# Moteurs 

global vitesse
global left_speed
global right_speed
vitesse = 0
left_speed = 0
right_speed = 0

###################################
########## Configuration ##########
###################################

url = "http://proj103.r2.enst.fr" #"https://comment.requestcatcher.com"
epreuve_intermediaire = True
no_logs = True

current_pos = Position_robot((25,25),(0,1))

last_analyse = ""
last_update_time = time.time()
users_connected = dict() 
cam = None 
image_view = True

aruco_detectes = []

c = controller.Controller()
c.standby()

CASE_MAX_DISTANCE = 75

################################################
######### Communication serveur suivi ##########
################################################

def send_position(x,y):
	#print(f"Sending request {url+f'/api/pos?x={x}&y={y}'}")
	r = requests.post(url+f"/api/pos?x={x}&y={y}")

	if r.status_code != 200: 
		#print(f"Failed to send data to server {r.status_code}")
		pass

def get_status():
	#print(f"Sending request {url+'/api/status'}")
	r = requests.get(url+"/api/status")
	if r.status_code != 200: 
		print(f"Failed to retrieve data from server {r.status_code}")
	else:
		return r.json()

def found_flag(marquer_id,col,row):
	print(f"Sending request {url+f'/api/marker?id={marquer_id}&col={col}&row={row}'}")
	r = requests.post(url+f"/api/marker?id={marquer_id}&col={col}&row={row}")

	if r.status_code != 200: 
		print(f"Failed to send data to server {r.status_code}")

################################################
######### Conversion cases/coord/autre #########
################################################

def cell_to_case(c):
	return (c.col,-c.row)

def case_to_cell(case):
	return Cell(case[1],case[0])

def case_to_pos(case):
	"""revoie la position (x,y) en centimètre du milieu de la case (i,j)"""
	i,j = case 
	return (25+int(i)*50, -25+int(j)*50)

def pos_to_case(pos):
	"""renvoie la case (i,j) à paritr de la pos (x,y)  en centimètres"""
	x,y = pos 
	return (int(x)//50, (25+int(y))//50)

def case_to_string(case):
	"""renvoie le string lettre+chiffre à partir de la case (i,j)"""
	i,j = case
	if not (0<=i<7 or 0<=j<7):
		print("Hors du terrain")
		return None
	string = "GFEDCBA"[int(j)]
	return (string,str(int(i)+1))

def string_to_case(case):
	"""renvoie la case (i,j) correspondant au string
	None si le format est incorrect"""
	j = "GFEDCBA".find(case[0])
	if j==-1:
		"gfedcba".find(case[0])
	return (int(case[1])-1,j)

################################################################################
################################################################################
################################################################################
################################################################################

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__, static_url_path='/static/')
if no_logs:
	log = logging.getLogger('werkzeug')
	log.disabled = True

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

@app.route('/', methods=['GET','POST'])
def page():
	return render_template("page.html")	

@app.route('/init_position', methods=['POST'])
def init_position():
	print("Request to /init_position")
	global current_pos, CASE_DEPART
	case_x = request.form.get('x')
	case_y = request.form.get('y')
	orientation = request.form.get('orientation')
	print(case_x,case_y,orientation)

	current_pos.set_pos(*case_to_pos(string_to_case((case_x,case_y))))
	if orientation is not None:
		current_pos.set_orientation(*vecteur_2d.rotate_vect((0,1),int(orientation)))

	send_position(*current_pos.get_pos())
	CASE_DEPART = case_to_cell(pos_to_case(current_pos.get_pos()))
	return render_template("page.html")	

@app.route('/toggle-image-view', methods=['POST'])
def toggle_image_view():
	print("Request to /toggle-image-view")
	global image_view
	image_view = not image_view
	return render_template("page.html")	


#####################################################
############### Contrôle manuelle ###################
#####################################################

@app.route('/change-speed', methods=['POST'])
def change_speed():
	print("Request to /change-speed")
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
	elif left_speed < 0 and right_speed < 0 and right_speed >= -vitesse:
		right_speed -= vitesse
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
	elif left_speed < 0 and right_speed < 0 and left_speed >= -vitesse:
		left_speed -= vitesse
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
	elif left_speed < 0 and right_speed < 0:
		right_speed += vitesse
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
	elif left_speed < 0 and right_speed < 0:
		left_speed += vitesse
	else:
		right_speed -= vitesse
	moteur.set_speed(int(left_speed), int(right_speed))
	return render_template("page.html")	


#####################################################
############### Contrôle autonôme ###################
#####################################################

@app.route('/go_to', methods=['POST'])
def go_to():
	print("Request to /go_to")
	global current_pos
	case_x = request.form.get('x')
	case_y = request.form.get('y')

	if not current_pos.is_moving():
		target_x, target_y = case_to_pos(string_to_case((case_x,case_y)))
		main.aller_case(target_x, target_y, current_pos)

	if epreuve_intermediaire:
		found_flag(5, target_x, target_y)
		moteur.tour_sur_soi_meme()

	return render_template("page.html")	

@app.route('/reperage-rotation', methods=['POST'])
def reperage_rotation_prep():
	print("Request to /reperage-rotation")
	global current_pos

	info_images = [] 
	orientations = []
	res = main.reperage_rotation(cam)
	for i in range(len(res)):
		img,orientation = res[i]
		module_camera.save_image(img,f"image{i}")
		info_images.append(analyse_image.detect_aruco_markers(img,current_pos))
		orientations.append(orientation)

	print(f"info image: {info_images}")
	res = position_from_arucos.get_position_from_markers(info_images)

	if res is None:
		print("No arucos found!")
		return None
	real_pos, err = res

	orientations_vect = []
	for i in range(len(info_images)):
		res = position_from_arucos.get_orientation(real_pos, info_images[i])
		if res is not None:
			orient_img, err = res
			orient = vecteur_2d.rotate_vect(orient_img,-orientations[i])
			orientations_vect.append(orient)

	if len(orientations_vect) != 0:
		orientation, _ = vecteur_2d.vect_mean(orientations_vect)
		current_pos.set_orientation(*orientation)
	
	current_pos.set_pos(*real_pos)

	send_position(*current_pos.get_pos())

	return render_template("page.html")	

@app.route('/test-aller-drap', methods=['POST'])
def aller_drap():
	print("Request to /test-aller-drap")
	image, result = module_camera.get_image(cam)
	list_aru = analyser_drapeau.drapeau_proche(analyse_image.detect_aruco_markers(image, current_pos))
	if list_aru is not None and len(list_aru) > 0: 
		print(analyser_drapeau.analyser_drapeau(list_aru, current_pos, cam))
	return render_template("page.html")	

@app.route('/test-ultime', methods=['POST'])
def ultime():
	print("Request to /test-ultime")
	nb_drapeaux = 2 
	for i in range(nb_drapeaux):
		#next_flag = None #info du aruco (id_marker, dist_marker, )
		flags = []
		while flags == []:
			angle = current_pos.get_angle_orientation()

			# S'orienter vers 90 (droit/est)
			if -45 < angle and angle < 45 :
				print("		"+"looking north")
				moteur.rota_deg(90, current_pos)
			elif -135 < angle and angle < -45 :
				print("		"+"looking west")
				moteur.rota_deg(180, current_pos)
			elif angle < -135 and angle >135 :
				print("		"+"looking south")
				moteur.rota_deg(-90, current_pos)
				
			curr_tick = [0,0]
			# Tourner 9 fois 
			for i in range(9):
				moteur.rota_petit_angle(i, curr_tick)
				current_pos.set_orientation(*vecteur_2d.rotate_vect((0,1),90-((curr_tick[1]*360)/(2*3.141592*7.85*183.6)-(curr_tick[0]*360)/(2*3.141592*7.85*183.6))/2))
				image, result = module_camera.get_image(cam)
				arus = analyse_image.detect_aruco_markers(image, current_pos)
				for j in range(len(arus)):
					print("		"+f"Aruco {arus[j][0]} found")
					if arus[j][0] not in [1,2,3,4]:
						print("		"+"it is a target")
						flags.append(arus[j])

			moteur.reajustement(curr_tick)
			moteur.rota_deg(-90,current_pos)
			current_pos.set_orientation(*vecteur_2d.rotate_vect((0,1),0))
					
			if flags!=[]:
				print("		"+f"flag found {flags}")
				#on cherche le flag le plus proche
				next_flag = analyser_drapeau.drapeau_proche(flags)
				print("		"+f"closet flag {next_flag[0]}")

				id_flag, coord_flag = analyser_drapeau.analyser_drapeau(next_flag, current_pos,cam)
				x_flag,y_flag = coord_flag

				x,y = current_pos.get_pos()
				print("		"+f" flag coords {x_flag} {y_flag}")
				if id_flag != -1:
					print("		"+f"!!! Flag Found !!! {id_flag} at coords {x_flag} {y_flag} by standing in {x} {y}")
					moteur.tour_sur_soi_meme()
					found_flag(id_flag, *case_to_string(pos_to_case((x, y))))

				
				main.aller_case(75,y_flag+25,current_pos)
			else:

				print("		"+"no flag found")
				x, y = current_pos.get_pos()
				main.aller_case(x, y + 100, current_pos)
	return render_template("page.html")	

#################################################
########### Config serveur commun ###############
#################################################

CASE_DEPART = None

def goto_case(case: Cell):
	print(f"Going to {cell_to_case(case)} ie {''.join(case_to_string(cell_to_case(case)))}")
	main.aller_case(*case_to_pos(cell_to_case(case)),current_pos)

def scan_direction(direction: Direction) -> Flag:
	target_angle = ( - 45 - 90 * direction.value) % 360
	# 0 3
	# 1 2 
	print(f"Scanning to {direction.value} -> {target_angle}")

	to_turn = (target_angle - current_pos.get_angle_orientation())%360
	print(to_turn, (360-to_turn)%360)
	if abs(to_turn) >= (360 - to_turn)%360:
		to_turn = -(360-to_turn)%360

	moteur.rota_deg(to_turn, current_pos)


	image, result = module_camera.get_image(cam)
	arus = analyse_image.detect_aruco_markers(image, current_pos)

	print(cel.row,cel.col)
	if len(arus) != 0:
		next_flag = analyser_drapeau.drapeau_proche(arus)

		id_flag, distance, _, _, coord_flag = next_flag
		print(f"Flag {id_flag} found at {coord_flag}, distance {distance}")

		if distance >= CASE_MAX_DISTANCE:
			print("Flag is too far away, not in adjacent cell")
		else:
			print("Sending flag to server")
			cel = case_to_cell(pos_to_case(current_pos.get_pos()))
			print(Flag(case_to_cell(pos_to_case(current_pos.get_pos())),direction,id_flag))
			return Flag(case_to_cell(pos_to_case(current_pos.get_pos())),direction,id_flag)

	print("No flag found")
	print(Flag(case_to_cell(pos_to_case(current_pos.get_pos())),direction,Flag.NO_FLAG))
	return Flag(case_to_cell(pos_to_case(current_pos.get_pos())),direction,Flag.NO_FLAG)

def capture(flag: Flag):
	print(f"Capturing {flag.id} at {cell_to_case(flag.cell)}")
	moteur.tour_sur_soi_meme()
	found_flag(flag.id, *case_to_string(pos_to_case(cell_to_case(flag.cell))))

@app.route('/master_control', methods=['POST'])
def await_instruction():
	print("Request to /master_control")
	for instruction in receive_instructions(CASE_DEPART):
		print("Instruction received")
		match instruction.type():
			case MsgType.INSTRUCTION_GOTO:
				goto_case(instruction.content)
			case MsgType.INSTRUCTION_SCAN:
				send_flag(scan_direction(instruction.content))
			case MsgType.INSTRUCTION_CAPTURE:
				capture(instruction.content)
		print("")
		print("Awaiting for instruction... ", end="")

################################################################################
################################################################################
################################################################################
################################################################################

@app.route('/update')
def update():
	global last_update_time, users_connected, cam, last_analyse, current_pos
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
			print("Camera not connected, Connecting to camera")
			cam = module_camera.connect()
		connexion = module_camera.check_camera_status(cam,verbose=False)
		updated_content+=f"<p>Connexion camera : {connexion}</p>"

	###### Code qui s'exécute toute les secondes #######
	if now - last_update_time >= 0.9:
		# Envoi vers l'api 
		send_position(*map(int,current_pos.get_pos()))
		#status = get_status()
		#found_flag(marquer_id, col, row)



		# Saving image
		if image_view:
			image, result = module_camera.get_image(cam)
			if result:
				module_camera.save_image(image)
				analyse = analyse_image.detect_aruco_markers(image,current_pos)
				last_analyse=""
				for a in analyse:
					last_analyse += f"<li>id:{a[0]} distance:{a[1]} angle:{a[2]} coord_centre:{a[3]} coord drapeau:{a[4]}</li>"
			else:
				print("Image did not save")

		last_update_time = now
	#####################################################

		
	# Contenu renvoyé
	updated_content+=f"<p>En mouvement: {current_pos.is_moving()}</p>"
	updated_content+=f"<p>État des moteurs {c.get_motor_speed()}</p>"
	updated_content+=f"<p>Vitesse actuelle: {vitesse}</p>"
	updated_content+=f"<p>Position actuelle (cm) x:{current_pos.get_pos()[0]} y:{current_pos.get_pos()[1]} angle:{current_pos.get_angle_orientation()}</p>"
	case_x,case_y= pos_to_case(current_pos.get_pos())
	str_x, str_y = case_to_string((case_x,case_y))
	updated_content+=f"<p>Position actuelle (case) {str_x}{str_y}</p>"
	updated_content+=f"<p>Host robot {host_robot}</p>"
	updated_content+=f"<p>Server url {url}</p>"
	updated_content+=f"<p>Analyse d'aruco:</p>"
	updated_content+=f"<ul>{last_analyse}</ul>"
	updated_content+=f"<p>Nombre d'utilisateurs connectés {len(users_connected)}</p>"
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

