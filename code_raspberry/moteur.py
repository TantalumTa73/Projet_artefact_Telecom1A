"""Les fonctions à utiliser pour déplacer le robot sont
	- avancer_cm
	- rota_deg
	"""

import controller as c
import time as t
import os 

# Moteurs 

moteur = c.Controller()
moteur.standby()
moteur.set_motor_shutdown_timeout(10)

def action_moteur(type_action):

	if type_action[0] == "r":

		dist = int(type_action[1:])
		# CALCUL SAVANT POUR CONVERTIR CENTIMETRE EN TICK
		avance_corrige("left", 1, dist)

def set_speed(lspeed, rspeed):
	moteur.set_motor_speed(lspeed, rspeed)

def acceleration(vitesse,time_step=0.01, temps_accel=2):

	""" Accélère de façon progressive jusqu'à une certaine vitesse """

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

def calc_tick_accel(vitesse, time_step=0.01, temps_accel=2):
	vitesse = int(vitesse)
	n = int(temps_accel/time_step)
	tick = 0
	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		tick += dvitesse*time_step*100
	return tick

def deceleration(vitesse,time_step=0.01, temps_decel=2):

	""" Décélère de façon progressive jusqu'à l'arrêt depuis une certaine vitesse """

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

def calc_tick_decel(vitesse, time_step=0.01, temps_accel=2):
	vitesse = int(vitesse)
	n = int(temps_accel/time_step)
	tick = 0
	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		tick += (vitesse-dvitesse)*time_step*100
	return tick

def straight_line(vitesse, time_step=0.01, temps=2):
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


	


def avance_corrige(moteur_princ, ratio, vitesse):

	""" Fait avancer le robot en imposant un ratio (entre 0 et 1) entre les vitesses des moteurs, 
		le moteur le plus rapide est moteur_prin entre left et right """

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

def avance_cm(dist, position_robot, time_step=0.01, temps_accel_decel=4):
	"""permet d'avancer le robot de dist cm"""
	if not position_robot.is_moving():
		position_robot.get_moving()

		ticks = int(dist * 183.6)
		"""asserv_decel = {10:30, 20:60, 30:80, 40:100, 50:115, 60:135, 70:155}"""
		poss_speed = [70, 60, 50, 40, 30, 20, 10]
		if dist < 0:
			ticks = -ticks
		for spd in poss_speed:
			#print('patate')
			acc_tick = calc_tick_accel(spd, time_step, temps_accel_decel)
			dec_tick = calc_tick_decel(spd, time_step, temps_accel_decel)
			tick_parc = ticks - acc_tick - dec_tick
			if tick_parc > 0:
				temps_parc = tick_parc/(100 * spd)
				if dist < 0:
					avance_asservi(-spd, time_step, temps_parc, temps_accel_decel, temps_accel_decel)
				else:
					avance_asservi(spd, time_step, temps_parc, temps_accel_decel, temps_accel_decel)
				break
		position_robot.avancer(dist)
		position_robot.stop_moving()
	else:
		print("erreur moteur.py, avance_cm : le robot est déjà en train d'avancer")

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


def rota_deg(deg, position_robot, time_step=0.01, temps_accel_decel=2):
	"""permet de tourner le robot de deg degrés dans le sens horaire"""
	if not position_robot.is_moving():
		position_robot.get_moving()
		side = "right"
		if deg < 0:
			deg = -deg
			side = "left"
		ticks = int((deg * 183.6 * 2 * 3.141592 * 7.85) / 360)
		poss_speed = [20,15,12,10,5,3]
		for spd in poss_speed:
			acc_tick = calc_tick_accel(spd, time_step, temps_accel_decel)
			dec_tick = calc_tick_decel(spd, time_step, temps_accel_decel)
			tick_parc = ticks - acc_tick - dec_tick
			if tick_parc > 0:
				temps_parc = tick_parc/(100 * spd)
				rotation_asservi(spd, time_step, temps_parc, temps_accel_decel, temps_accel_decel, side)
				break
		moteur.set_motor_speed(0,0)

		if side == "right":
			position_robot.tourner(deg)
		else:
			position_robot.tourner(-deg)
		position_robot.stop_moving()

		t.sleep(1)
	else:
		print("erreur moteur.py, rota_deg : le robot est déjà en train d'avancer")


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
		acc_tick_left = calc_tick_accel(left_speed, time_step, temps_accel)
		dec_tick_left = calc_tick_decel(left_speed, time_step, temps_decel)
		acc_tick_right = calc_tick_accel(right_speed, time_step, temps_accel)
		dec_tick_right = calc_tick_decel(right_speed, time_step, temps_decel)
		tick_parc_left = - supposed_ticks_turn[l] - curr_tick[0] - acc_tick_left - dec_tick_left
		tick_parc_right = supposed_ticks_turn[l] - curr_tick[1] - acc_tick_right - dec_tick_right
		if tick_parc_left < 0 and tick_parc_right > 0:
			temps_parc = tick_parc_left/(left_speed*100)
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
		acc_tick_left = calc_tick_accel(left_speed, time_step, temps_accel)
		dec_tick_left = calc_tick_decel(left_speed, time_step, temps_decel)
		acc_tick_right = calc_tick_accel(right_speed, time_step, temps_accel)
		dec_tick_right = calc_tick_decel(right_speed, time_step, temps_decel)
		tick_parc_left = - tot_tick[0] - acc_tick_left - dec_tick_left
		tick_parc_right = tot_tick[1] - acc_tick_right - dec_tick_right
		if tick_parc_left < 0 and tick_parc_right > 0:
			temps_parc = tick_parc_left/(left_speed*100)
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

			print( n_accel , n_decel , n_parcours)
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

def tour_sur_soi_meme():
	turntick = int(183.6 * 2 * 3.141592 * 7.85)
	reajustement([-turntick, turntick])


def avance_tick(position_robot, tick_left, tick_right, time_step = 0.01):
	poss_speed = [70, 60, 50, 40, 30, 20, 15, 10, 5, 3]
	temps_accel_decel = {70: 3.5, 60: 3, 50: 2.5, 40: 2, 30: 1.5, 20: 1, 15: 0.75, 10: 0.5, 5: 0.25, 3: 0}
	ticks = moteur.get_encoder_ticks()
	position_robot.add_tick_offset(ticks)
	ticks = position_robot.get_tick_offset()
	tick_left += - ticks[0]
	tick_right += - ticks[1]
	forward = tick_left > 0
	curr_tick = [0,0]
	ratio = tick_left / tick_right
	for spd in poss_speed: 
		if forward:
			left_speed = spd
		else:
			left_speed = - spd
		right_speed = ratio * left_speed
 		acc_tick_left = calc_tick_accel(left_speed, time_step, temps_accel_decel[spd])
		dec_tick_left = calc_tick_decel(left_speed, time_step, temps_accel_decel[spd])
		acc_tick_right = calc_tick_accel(right_speed, time_step, temps_accel_decel[spd])
		dec_tick_right = calc_tick_decel(right_speed, time_step, temps_accel_decel[spd])
		tick_parc_left = tick_left - acc_tick_left - dec_tick_left
		tick_parc_right = tick_right - acc_tick_right - dec_tick_right
		if tick_parc_left < 0 and tick_parc_right > 0:
			temps_parc = tick_parc_left/(left_speed*100)
			n_accel = int(temps_accel_decel[spd]/time_step)
			n_parcours = int(temps_parc/time_step)
			n_decel = int(temps_accel_decel[spd]/time_step)
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

			print( n_accel , n_decel , n_parcours)
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
