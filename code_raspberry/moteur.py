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

def acceleration(vitesse,time_step, temps_accel):

	""" Accélère de façon progressive jusqu'à une certaine vitesse """

	vitesse = int(vitesse)
	n = int(temps_accel/time_step)

	curr_ticks = [0,0]
	supposed_ticks = [0]

	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		supposed_ticks.append(dvitesse*time_step*100 + supposed_ticks[-1])
	print(supposed_ticks)

	for k in range(0,n + 1):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		print("curr", curr_ticks)     
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1], curr_ticks

def calc_tick_accel(vitesse, time_step, temps_accel):
	vitesse = int(vitesse)
	n = int(temps_accel/time_step)
	tick = 0
	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		tick += dvitesse*time_step*100
	return tick

def deceleration(vitesse,time_step, temps_decel):

	""" Décélère de façon progressive jusqu'à l'arrêt depuis une certaine vitesse """

	vitesse = int(vitesse)
	n = int(temps_decel/time_step)

	curr_ticks = [0,0]
	supposed_ticks = [0]

	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		supposed_ticks.append((vitesse -dvitesse)*time_step*100 + supposed_ticks[-1])
	print(supposed_ticks)

	for k in range(0,n + 1):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]      
		print("curr", curr_ticks)     
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100)) + 3
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100)) + 3
		print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1], curr_ticks

def calc_tick_decel(vitesse, time_step, temps_accel):
	vitesse = int(vitesse)
	n = int(temps_accel/time_step)
	tick = 0
	for k in range(0, n + 1):
		dvitesse = int(k * vitesse / n)
		tick += (vitesse-dvitesse)*time_step*100
	return tick

def straight_line(vitesse, time_step, temps):
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
		print("curr", curr_ticks)     
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100)) + 3
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100)) + 3
		print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1], curr_ticks


    


def avance_corrige(moteur_princ, ratio, vitesse):

	""" Fait avancer le robot en imposant un ratio (entre 0 et 1) entre les vitesses des moteurs, 
		le moteur le plus rapide est moteur_prin entre left et right """

	ratio = float(ratio)
	vitesse = int(vitesse)

	if moteur_princ == "left":

		print("C presque ça")
		print(moteur_princ, ratio, vitesse)
		print(moteur.get_encoder_ticks())
		print("test")
		acceleration(vitesse)
		moteur.set_motor_speed(vitesse, int(ratio * vitesse))
		t.sleep(2)
		print(moteur.get_encoder_ticks())
	else:

		moteur.set_motor_speed(int(ratio * vitesse), vitesse)

def rotation_test(temps, vitesse, côté):
	if côté == "left":
		vitesse = -vitesse
	moteur.set_motor_speed(vitesse, -vitesse)
	t.sleep(temps)
	print(moteur.get_encoder_ticks())
	
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

	print(val[1::])
	print(sum(map(lambda x : x[0], val[1::])))
	print(sum(map(lambda x : x[1], val[1::])))
	print()
	print(real_ticks)
	print(sum(real_ticks))

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
		dvitesse = int(k * vitesse / n_decel)
		supposed_ticks.append((vitesse -dvitesse)*time_step*100 + supposed_ticks[-1])
	print(supposed_ticks)

	for k in range(0, n_accel + n_parcours + n_decel + 2):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		print("curr", curr_ticks)     
		speed_left = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		print("tickgap", supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	moteur.set_motor_speed(0,0)
	print([supposed_ticks[-1], curr_ticks])

def avance_cm(dist, time_step, temps_accel_decel):
	ticks = int(dist * 185.72)
	asserv_decel = {10:30, 20:60, 30:80, 40:100, 50:115, 60:135, 70:155}
	poss_speed = [70, 60, 50, 40, 30, 20, 10]
	for spd in poss_speed:
		print('patate')
		acc_tick = calc_tick_accel(spd, time_step, temps_accel_decel)
		dec_tick = calc_tick_decel(spd, time_step, temps_accel_decel)
		tick_parc = ticks - acc_tick - dec_tick - asserv_decel[spd]
		if tick_parc > 0:
			temps_parc = tick_parc/(100 * spd)
			avance_asservi(spd, time_step, temps_parc, temps_accel_decel, temps_accel_decel)
			break
        
def rotation_asservi(vitesse, time_step, temps_parcours, temps_accel, temps_decel, side):
	if side == "right":
		vitesse = - vitesse
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
		dvitesse = int(k * vitesse / n_decel)
		supposed_ticks.append((vitesse -dvitesse)*time_step*100 + supposed_ticks[-1])
	print(supposed_ticks)

	for k in range(0, n_accel + n_parcours + n_decel + 2):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		print("curr", curr_ticks)     
		speed_left = int((- supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_right = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		print("tickgap",  - supposed_ticks[k+1] - curr_ticks[0], supposed_ticks[k+1] - curr_ticks[1])
		print("speed", [speed_left, speed_right])
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	moteur.set_motor_speed(0,0)
	print([supposed_ticks[-1], curr_ticks])


def rota_deg(deg, time_step, temps_accel_decel):
	deg = deg%360
	side = "right"
	if deg > 180:
		deg = 360 - deg
		side = "left"
	print(deg)
	ticks = int((deg * 185.72 * 2 * 3.141592 * 7.85) / 360)
	print(ticks)
	asserv_decel = {10:240}
	poss_speed = [10]
	for spd in poss_speed:
		print('patate')
		acc_tick = calc_tick_accel(spd, time_step, temps_accel_decel)
		dec_tick = calc_tick_decel(spd, time_step, temps_accel_decel)
		tick_parc = ticks - acc_tick - dec_tick - asserv_decel[spd]
		print(tick_parc)
		if tick_parc > 0:
			temps_parc = tick_parc/(100 * spd)
			rotation_asservi(spd, time_step, temps_parc, temps_accel_decel, temps_accel_decel, side)
			break