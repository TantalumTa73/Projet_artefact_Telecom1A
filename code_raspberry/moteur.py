"""Les fonctions à utiliser pour déplacer le robot sont
	- avancer_cm
	- rota_deg
	"""

import controller as c
import time as t
import os 

# Moteurs 

def setup():
	global moteur
moteur = c.Controller()
moteur.standby()
moteur.set_motor_shutdown_timeout(10)

TIMESTEP = 0.01 #Correspond à la fréquence de mise à jour de la vitesse des roues pendant l'asservissement
PI = 3.141592 
CM_TO_TICK = 183.6 #Nombre de ticks de roue nécessaires pour parcourir un cm à l'aide du robot
DIST_INTER_ROUES = 7.85 #Demi-distance entre les deux roues, permettant notamment de connaitre le nombre de ticks nécessaires pour faire tourner le robot
						#d'un nombre donné de degrés 

MIN_SPEED = 1
#### Début de code, non utilisé durant les évaluations ####

def set_speed(lspeed, rspeed):
	moteur.set_motor_speed(lspeed, rspeed)
"""
def action_moteur(type_action):

	if type_action[0] == "r":

		dist = int(type_action[1:])
		# CALCUL SAVANT POUR CONVERTIR CENTIMETRE EN TICK
		avance_corrige("left", 1, dist)

def acceleration(vitesse,time_step=0.01, temps_accel=2):

	#Accélère de façon progressive jusqu'à une certaine vitesse

	vitesse = int(vitesse)
	n = int(temps_accel/time_step)

	curr_ticks = [0,0]
	supposed_ticks = [0]

	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		supposed_ticks.append(dvitesse*time_step*100 + supposed_ticks[-1])
	#print(supposed_ticks)

	for k in range(0,n + 1):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		#print("curr", curr_ticks)	 
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		#print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		#print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1], curr_ticks

def deceleration(vitesse,time_step=0.01, temps_decel=2):

	#Décélère de façon progressive jusqu'à l'arrêt depuis une certaine vitesse

	vitesse = int(vitesse)
	n = int(temps_decel/time_step)

	curr_ticks = [0,0]
	supposed_ticks = [0]

	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		supposed_ticks.append((vitesse -dvitesse)*time_step*100 + supposed_ticks[-1])
	#print(supposed_ticks)

	for k in range(0,n + 1):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]	  
		#print("curr", curr_ticks)	 
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100)) + 3
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100)) + 3
		#print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		#print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1], curr_ticks
	
	
def straight_line(vitesse, time_step, temps=2):
	n = int(temps / time_step)
	real_ticks = 0
	curr_ticks = [0,0]
	supposed_ticks = [0]

	for k in range(0,n):
		supposed_ticks.append(vitesse*time_step*100 + supposed_ticks[-1])

	for k in range(0,n):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		#print("curr", curr_ticks)	 
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100)) + 3
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100)) + 3
		#print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		#print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1], curr_ticks
"""

def calc_tick_accel(vitesse, time_step, temps_accel):
	n = round(temps_accel/time_step)
	tick = 0
	tick_parc = 0
	n_debut = 0
	for k in range(0, n + 1):
		dvitesse = (k * vitesse / n)
		if abs(dvitesse) < MIN_SPEED:
			tick_parc += dvitesse*time_step*100
		else: 
			if n_debut == 0:
				n_debut = k
			tick += dvitesse*time_step*100
	return tick, n_debut

def calc_tick_decel(vitesse, time_step, temps_accel):
	n = round(temps_accel/time_step)
	tick = 0
	tick_parc = 0
	n_fin = 0
	for k in range(0, n + 1):
		dvitesse = (k * vitesse / n)
		if abs(vitesse - dvitesse) < MIN_SPEED:
			if n_fin == 0:
				n_fin = k
			tick_parc += (vitesse - dvitesse)*time_step*100
		else: 
			tick += (vitesse - dvitesse)*time_step*100
	return tick, n_fin


#### Tentative de correction de la différence de vitesse entre les deux roues ####

"""

def avance_corrige(moteur_princ, ratio, vitesse):

	#Fait avancer le robot en imposant un ratio (entre 0 et 1) entre les vitesses des moteurs, 
	#	le moteur le plus rapide est moteur_prin entre left et right

	ratio = float(ratio)
	vitesse = int(vitesse)

	if moteur_princ == "left":

		#print("C presque ça")
		#print(moteur_princ, ratio, vitesse)
		#print(moteur.get_encoder_ticks())
		#print("test")
		acceleration(vitesse)
		moteur.set_motor_speed(vitesse, int(ratio * vitesse))
		t.sleep(2)
		#print(moteur.get_encoder_ticks())
	else:

		moteur.set_motor_speed(int(ratio * vitesse), vitesse)

def rotation_test(temps, vitesse, côté):
	if côté == "left":
		vitesse = -vitesse
	moteur.set_motor_speed(vitesse, -vitesse)
	t.sleep(temps)
	#print(moteur.get_encoder_ticks())
	
def avance_test():
	moteur.set_motor_shutdown_timeout(10)

	# 1,3,30,0.1
	temps_parcours, vitesse, time_step, temps_accel, temps_decel = (10,30,0.1,0.5,0.5) #*sys.argv[1::]

	val = []
	real_ticks = [] 
	
	val.append(moteur.get_encoder_ticks())
	res = acceleration(vitesse,time_step, temps_accel)
	real_ticks.append(res[0])
	val.append(res[1])
	val.append(moteur.get_encoder_ticks())
	res = straight_line(vitesse,time_step*0.1,temps_parcours)
	real_ticks.append(res[0])
	val.append(res[1])
	val.append(moteur.get_encoder_ticks())
	res = deceleration(vitesse,time_step, temps_decel)
	real_ticks.append(res[0])
	val.append(res[1])
	val.append(moteur.get_encoder_ticks())
	moteur.set_motor_speed(0,0)

	#print(val[1::])
	#print(sum(map(lambda x : x[0], val[1::])))
	#print(sum(map(lambda x : x[1], val[1::])))
	#print()
	#print(real_ticks)
	#print(sum(real_ticks))

"""


#### Diverses fonctions d'asservissement, utilisés pour passer l'évaluation intérmédiaire avec brio ####
#Le seul point faible était le manque de généralité de l'asservissement, ce dernier fonctionnait lorsque l'on faisait les déplacements mais ne 
#prenait pas en compte les petites incertitudes d'un déplacement à l'autre

"""
def avance_asservi(vitesse, time_step, temps_parcours, temps_accel, temps_decel):
	moteur.get_encoder_ticks()
	vitesse = int(vitesse)
	n_accel = int(temps_accel/time_step)
	n_decel = int(temps_decel/time_step)
	n_parcours = int(temps_parcours/time_step)
	real_ticks = 0
	curr_ticks = [0,0]
	supposed_ticks = [0]
	for k in range(0,n_accel + 1):
		dvitesse = int(k * vitesse / n_accel)
		supposed_ticks.append(dvitesse*time_step*100 + supposed_ticks[-1])
	for k in range(0,n_parcours):
		supposed_ticks.append(dvitesse*time_step*100 + supposed_ticks[-1])
	for k in range(0,n_decel + 1):
		dvitesse = k * vitesse / n_decel
		supposed_ticks.append((vitesse -dvitesse)*time_step*100 + supposed_ticks[-1])
	#print(supposed_ticks)

	for k in range(0, n_accel + n_parcours + n_decel + 2):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		#print("curr", curr_ticks)	 
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		#print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		#print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	moteur.set_motor_speed(0,0)
	#print([supposed_ticks[-1], curr_ticks])

def rotation_asservi(vitesse, time_step, temps_parcours, temps_accel, temps_decel, side):
	if side == "right":
		vitesse = - vitesse
	moteur.get_encoder_ticks()
	vitesse = vitesse
	n_accel = int(temps_accel/time_step)
	n_decel = int(temps_decel/time_step)
	n_parcours = int(temps_parcours/time_step)
	real_ticks = 0
	curr_ticks = [0,0]
	supposed_ticks = [0]
	for k in range(0,n_accel + 1):
		dvitesse = k * vitesse / n_accel
		supposed_ticks.append(dvitesse*time_step*100 + supposed_ticks[-1])
	for k in range(0,n_parcours):
		supposed_ticks.append(dvitesse*time_step*100 + supposed_ticks[-1])
	for k in range(0,n_decel + 1):
		dvitesse = k * vitesse / n_decel
		supposed_ticks.append((vitesse -dvitesse)*time_step*100 + supposed_ticks[-1])
	#print(supposed_ticks)

	for k in range(0, n_accel + n_parcours + n_decel + 2):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		#print("curr", curr_ticks)	 
		speed_left = int((- supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		#print("tickgap",  - supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		#print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	moteur.set_motor_speed(0,0)
	t.sleep(0.5)
	return([supposed_ticks[-1], curr_ticks])

def rota_petit_angle(l, curr_tick, time_step=0.01, temps_accel=1.5, temps_decel=1.5):
	ticks = moteur.get_encoder_ticks()
	curr_tick[0] += ticks[0]
	curr_tick[1] += ticks[1]
	tot_tick = int(183.6 * 2 * 3.141592 * 7.85)
	tick_per_turn = tot_tick/16
	supposed_ticks_turn = [tick_per_turn * i for i in range(17)]
	poss_speed = [20,15,10,5,3]
	curr_ticks_ins = [0,0]
	for spd in poss_speed:
		if curr_tick[0] == 0 :
			ratio = 1
		else:
			ratio = (supposed_ticks_turn[l] - curr_tick[1]) / (supposed_ticks_turn[l] + curr_tick[0])
		left_speed = - spd
		right_speed = ratio * spd
		left_acc_tick = calc_tick_accel(left_speed, time_step, temps_accel)
		left_dec_tick = calc_tick_decel(left_speed, time_step, temps_decel)
		right_acc_tick = calc_tick_accel(right_speed, time_step, temps_accel)
		right_dec_tick = calc_tick_decel(right_speed, time_step, temps_decel)

		left_parc_tick = - supposed_ticks_turn[l] - curr_tick[0] - left_acc_tick - left_dec_tick
		right_parc_tick = supposed_ticks_turn[l] - curr_tick[1] - right_acc_tick - right_dec_tick

		if left_parc_tick < 0 and right_parc_tick > 0:
			temps_parc = left_parc_tick/(left_speed*100)
			n_accel = int(temps_accel/time_step)
			n_parcours = int(temps_parc/time_step)
			n_decel = int(temps_decel/time_step)
			real_ticks = [0,0]
			curr_ticks_ins = [0,0]
			supposed_ticks = [[0,0]]
			for k in range(0,n_accel + 1):
				dvitesse_left = k * left_speed / n_accel
				dvitesse_right = k * right_speed / n_accel
				supposed_ticks.append([dvitesse_left*time_step*100 + supposed_ticks[-1][0], dvitesse_right*time_step*100 + supposed_ticks[-1][1]])
			for k in range(0,n_parcours):
				supposed_ticks.append([left_speed*time_step*100 + supposed_ticks[-1][0], right_speed*time_step*100 + supposed_ticks[-1][1]])
			for k in range(0,n_decel + 1):
				dvitesse_left = k * left_speed / n_decel
				dvitesse_right = k * right_speed / n_decel
				supposed_ticks.append([(left_speed - dvitesse_left)*time_step*100 + supposed_ticks[-1][0], (right_speed - dvitesse_right)*time_step*100 + supposed_ticks[-1][1]])

			for k in range(0, n_accel + n_decel + n_parcours  + 2):
				ticks = moteur.get_encoder_ticks()
				curr_ticks_ins[0] += ticks[0]
				curr_ticks_ins[1] += ticks[1]   
				speed_left = int((supposed_ticks[k+1][0] - curr_ticks_ins[0]) / (time_step * 100))
				speed_right = int((supposed_ticks[k+1][1] - curr_ticks_ins[1]) / (time_step * 100))
				moteur.set_motor_speed(speed_left, speed_right)
				t.sleep(time_step)
			moteur.set_motor_speed(0,0)
			t.sleep(0.5)
			curr_tick[0] += curr_ticks_ins[0]
			curr_tick[1] += curr_ticks_ins[1]
			#print([(curr_tick[0]*360)/(2*3.141592*7.85*183.6), (curr_tick[1]*360)/(2*3.141592*7.85*183.6)])
			t.sleep(0.5)
			break

def reajustement(curr_tick, time_step=0.01, temps_accel=3, temps_decel=3):
	turntick = int(183.6 * 2 * 3.141592 * 7.85)
	tot_tick = [2 * turntick + curr_tick[0] , 2 * turntick - curr_tick[1]]
	moteur.get_encoder_ticks()
	poss_speed = [20,15,10,5,3]
	for spd in poss_speed:
		ratio = tot_tick[1]/tot_tick[0]
		left_speed = - spd
		right_speed = ratio * spd
		left_acc_tick = calc_tick_accel(left_speed, time_step, temps_accel)
		left_dec_tick = calc_tick_decel(left_speed, time_step, temps_decel)
		right_acc_tick = calc_tick_accel(right_speed, time_step, temps_accel)
		right_dec_tick = calc_tick_decel(right_speed, time_step, temps_decel)
		left_parc_tick = - tot_tick[0] - left_acc_tick - left_dec_tick
		right_parc_tick = tot_tick[1] - right_acc_tick - right_dec_tick
		if left_parc_tick < 0 and right_parc_tick > 0:
			temps_parc = left_parc_tick/(left_speed*100)
			n_accel = int(temps_accel/time_step)
			n_parcours = int(temps_parc/time_step)
			n_decel = int(temps_decel/time_step)
			curr_ticks_ins = [0,0]
			supposed_ticks = [[0,0]]
			for k in range(0,n_accel + 1):
				dvitesse_left = k * left_speed / n_accel
				dvitesse_right = k * right_speed / n_accel
				supposed_ticks.append([dvitesse_left*time_step*100 + supposed_ticks[-1][0], dvitesse_right*time_step*100 + supposed_ticks[-1][1]])
			for k in range(0,n_parcours):
				supposed_ticks.append([left_speed*time_step*100 + supposed_ticks[-1][0], right_speed*time_step*100 + supposed_ticks[-1][1]])
			for k in range(0,n_decel + 1):
				dvitesse_left = k * left_speed / n_decel
				dvitesse_right = k * right_speed / n_decel
				supposed_ticks.append([(left_speed - dvitesse_left)*time_step*100 + supposed_ticks[-1][0], (right_speed - dvitesse_right)*time_step*100 + supposed_ticks[-1][1]])

			#print( n_accel , n_decel , n_parcours)
			for k in range(0, n_accel + n_decel + n_parcours  + 2):
				ticks = moteur.get_encoder_ticks()
				curr_ticks_ins[0] += ticks[0]
				curr_ticks_ins[1] += ticks[1]   
				speed_left = int((supposed_ticks[k+1][0] - curr_ticks_ins[0]) / (time_step * 100))
				speed_right = int((supposed_ticks[k+1][1] - curr_ticks_ins[1]) / (time_step * 100))
				moteur.set_motor_speed(speed_left, speed_right)
				t.sleep(time_step)
			moteur.set_motor_speed(0,0)
			t.sleep(0.5)
			curr_tick[0] += curr_ticks_ins[0]
			curr_tick[1] += curr_ticks_ins[1]
			#print([(curr_tick[0]*360)/(2*3.141592*7.85*183.6), (curr_tick[1]*360)/(2*3.141592*7.85*183.6)])
			t.sleep(0.5)
			break
"""

def avance_cm(dist, position_robot, time_step=TIMESTEP):
	#permet d'avancer le robot de dist cm
	if not position_robot.is_moving():
		position_robot.get_moving()

		ticks = round(dist * CM_TO_TICK)
		avance_tick(position_robot, ticks, ticks)

		position_robot.avancer(dist)
		position_robot.stop_moving()
	else:
		print("erreur moteur.py, avance_cm : le robot est déjà en train d'avancer")

def rota_deg(deg, position_robot, time_step=TIMESTEP):
	#permet de tourner le robot de deg degrés dans le sens horaire
	if not position_robot.is_moving():
		position_robot.get_moving()
		side = "right"
		if deg < 0:
			deg = -deg
			side = "left"
		ticks = round(CM_TO_TICK * (2 * PI * DIST_INTER_ROUES) * (deg / 360)) #calcul simple du perimètre avec 2*pi*r

		if side == "right":
			avance_tick(position_robot, ticks, -ticks)
			moteur.set_motor_speed(0,0)
			position_robot.tourner(deg)
		else:
			avance_tick(position_robot, -ticks, ticks)
			moteur.set_motor_speed(0,0)
			position_robot.tourner(-deg)
		position_robot.stop_moving()

		t.sleep(1)
	else:
		print("erreur moteur.py, rota_deg : le robot est déjà en train d'avancer")


def tour_sur_soi_meme(position_robot):
	turntick = round(CM_TO_TICK * (2 * PI * DIST_INTER_ROUES))
	avance_tick(position_robot, turntick, -turntick)
	#reajustement([-turntick, turntick])


def avance_tick(position_robot, left_tick, right_tick, time_step = 0.01):
	#print(f"avance_tick {left_tick} {right_tick}")

	ticks = moteur.get_encoder_ticks()
	position_robot.add_tick_offset(ticks) #Le nombre de ticks en offset par rapport aux déplacements idéaux est gardé en mémoire, afin de pouvoir le 
	#corriger à chaque déplacement, c'est ce qui permet une cohérence entre l'asservissement d'un déplacement à l'autre

	ticks = position_robot.get_tick_offset()
	left_tick += - ticks[0]
	right_tick += - ticks[1]

	position_robot.set_tick_offset([0,0])

	#print(f"ticks {ticks}")
	#print(f"corrected ticks {left_tick} {right_tick}")


	forward_left = left_tick > 0
	forward_right = right_tick > 0

	if forward_left == forward_right:
		poss_speed = [40, 30, 20, 15, 10, 5] #Tableau des différentes vitesses que le robot peut prendre, on les limite afin de ne pas avoir
		#à tester toutes les vitesses entre 70 et 0
		temps_accel_decel = {40: 3, 30: 2.5, 20: 2, 15: 1.75, 10: 1.5, 5: 1.25} #Les temps d'accélération et de décélération
		#dépendent de la vitesse, l'objectif principal de l'asservissement est de capper l'accélération
	else:
		# On essaye de tourner 
		poss_speed = [30, 20, 15, 10, 5, 3] #Tableau des différentes vitesses que le robot peut prendre, on les limite afin de ne pas avoir
		temps_accel_decel = {30: 3.5, 20: 3, 15: 2.75, 10: 2.5, 5: 2.25, 3: 1.5} #Les temps d'accélération et de décélération

	for spd in poss_speed: 
		if forward_left:
			left_speed = spd
		else:
			left_speed = - spd

		if left_tick != 0:
			right_speed = (right_tick * left_speed) / left_tick
		else: 
			right_speed = 0
		#le principe ici est simple, on regarde toutes les vitesses que l'on peut prendre, on set ces vitesses sur la roue gauche, la vitesse de la roue
		#droite est ensuite déterminé par le ratio de distance qu'elle a à parcourir par rapport à l'autre roue (notamment si les deux roues tournent
		# dans des sens opposés, le ratio est négatif)

		left_acc_tick, ndal = calc_tick_accel(left_speed, time_step, temps_accel_decel[spd])
		left_dec_tick, nddl = calc_tick_decel(left_speed, time_step, temps_accel_decel[spd])
		right_acc_tick, ndar = calc_tick_accel(right_speed, time_step, temps_accel_decel[spd])
		right_dec_tick, nddr = calc_tick_decel(right_speed, time_step, temps_accel_decel[spd])
		#calcul des ticks pris sur le déplacement total par l'accélération et la décélération

		left_parc_tick = left_tick - left_acc_tick - left_dec_tick
		right_parc_tick = right_tick - right_acc_tick - right_dec_tick

		left_legit = (not(forward_left) and left_parc_tick < 0) or (forward_left and left_parc_tick > 0)
		right_legit = (not(forward_right) and right_parc_tick < 0) or (forward_right and right_parc_tick > 0)
		
		#On vérifie juste que le nombre de ticks en cumulé de l'accélération et la décélération ne dépasse pas le nombre de ticks total, et donc que la roue
		#ne change pas de sens en plein milieu du mouvement théorique, si la roue change de sens, on baisse la vitesse en continuant la boucle for
		if left_legit and right_legit:
			temps_parc = left_parc_tick/(left_speed*100)
			n_accel_decel = round(temps_accel_decel[spd]/time_step)
			n_accel = min(ndal, ndar)
			n_decel = max(nddl, nddr)
			n_parcours = round(temps_parc/time_step)
			curr_ticks_reel = [0,0] #Correspond au nombre de ticks que le robot a parcouru depuis le début du déplacement (roue gauche et droite)
			supposed_ticks = [[0,0]] #C'est un trajet théorique, à chaque instant dt(= TIMESTEP), on annonce au robot qu'il doit atteindre un certain nombre de 
			#ticks en dt, cela lui permet d'ajuster sa vitesse en fonction de s'il est en avance ou en retard

			#Construction du trajet théorique
			for k in range(n_accel,n_accel_decel + 1):
				dvitesse_left = (k * left_speed / n_accel_decel)
				dvitesse_right =(k * right_speed / n_accel_decel)
				if abs(dvitesse_left) < MIN_SPEED:
					dvitesse_left = 0
				if abs(dvitesse_right) < MIN_SPEED:
					dvitesse_right = 0
				supposed_ticks.append([dvitesse_left*time_step*100 + supposed_ticks[-1][0], dvitesse_right*time_step*100 + supposed_ticks[-1][1]])

			for k in range(0,n_parcours):
				supposed_ticks.append([left_parc_tick/n_parcours + supposed_ticks[-1][0], right_parc_tick/n_parcours + supposed_ticks[-1][1]])

			for k in range(0, n_decel):
				dvitesse_left = (k * left_speed / n_accel_decel)
				dvitesse_right =(k * right_speed / n_accel_decel)
				if abs(left_speed - dvitesse_left) < MIN_SPEED:
					dvitesse_left = left_speed
				if abs(right_speed - dvitesse_right) < MIN_SPEED:
					dvitesse_right = right_speed
				supposed_ticks.append([(left_speed - dvitesse_left)*time_step*100 + supposed_ticks[-1][0], (right_speed - dvitesse_right)*time_step*100 + supposed_ticks[-1][1]])

			#print(list(map(lambda x : list(map(int, x)),supposed_ticks)))
			#print(supposed_ticks[-1])
			#print(left_tick,right_tick)

			#On parcourt le trajet théorique
			for k in range(0, len(supposed_ticks)-1):

				#On update les ticks réels du robot, afin qu'il puisse se placer dans le trajet théorique
				ticks = moteur.get_encoder_ticks()

				curr_ticks_reel[0] += ticks[0]
				curr_ticks_reel[1] += ticks[1]
				
				#La vitesse des roues correspond simplement à la distance qu'ils doivent parcourir (distance qu'ils doivent atteindre - distance qu'ils ont déja parcouru)
				#que l'on divise ensuite par le dt (= TIMESTEP)
				speed_left = round((supposed_ticks[k+1][0] - curr_ticks_reel[0]) / (time_step * 100))
				speed_right = round((supposed_ticks[k+1][1] - curr_ticks_reel[1]) / (time_step * 100))
				moteur.set_motor_speed(speed_left, speed_right)
				t.sleep(time_step)
			moteur.set_motor_speed(0,0)
			t.sleep(1.5)
			ticks = list(moteur.get_encoder_ticks())
			curr_ticks_reel[0] += ticks[0]
			curr_ticks_reel[1] += ticks[1]   

			ticks[0] = curr_ticks_reel[0] - left_tick
			ticks[1] = curr_ticks_reel[1] - right_tick

			#print(f"ticks {ticks}")
			position_robot.set_tick_offset(ticks)
			#print("\n")
			break

