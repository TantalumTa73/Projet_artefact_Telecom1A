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

def acceleration(vitesse,time_step):

	""" Accélère de façon progressive jusqu'à une certaine vitesse """

	vitesse = int(vitesse)

	curr_ticks = [0,0]
	supposed_ticks = [0]

	for k in range(0, 11):
		dvitesse = int(k * vitesse / 10)
		supposed_ticks.append(dvitesse*time_step*100 + supposed_ticks[-1])
	print(supposed_ticks)

	for k in range(0,11):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]
		print(curr_ticks)     
		speed_right = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_left = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1]

def deceleration(vitesse,time_step):

	""" Décélère de façon progressive jusqu'à l'arrêt depuis une certaine vitesse """

	vitesse = int(vitesse)

	curr_ticks = [0,0]
	supposed_ticks = [0]

	for k in range(0, 11):
		dvitesse = int(k * vitesse / 10)
		supposed_ticks.append((vitesse -dvitesse)*time_step*100 + supposed_ticks[-1])
	print(supposed_ticks)

	for k in range(0,11):
		ticks = moteur.get_encoder_ticks()
		curr_ticks[0] += ticks[0]
		curr_ticks[1] += ticks[1]      
		speed_right = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_left = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1]

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
		speed_right = int((supposed_ticks[k+1] - curr_ticks[0]) / (time_step * 100))
		speed_left = int((supposed_ticks[k+1] - curr_ticks[1]) / (time_step * 100))
		moteur.set_motor_speed(speed_left, speed_right)
		t.sleep(time_step)
	return supposed_ticks[-1]


    


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
	attente, temps_parcours, vitesse, time_step = (1.1,3,30,0.1) #*sys.argv[1::]

	val = []
	real_ticks = [] 
	
	val.append(moteur.get_encoder_ticks())
	real_ticks.append(acceleration(vitesse,time_step))
	t.sleep(attente)
	val.append(moteur.get_encoder_ticks())
	moteur.set_motor_speed(0,0)
	"""val.append(moteur.get_encoder_ticks())
	real_ticks.append(straight_line(vitesse,time_step*3,temps_parcours))
	val.append(moteur.get_encoder_ticks())
	real_ticks.append(deceleration(vitesse,time_step))
	t.sleep(attente)
	val.append(moteur.get_encoder_ticks())
	moteur.set_motor_speed(0,0)"""

	print(val[1::])
	print(sum(map(lambda x : x[0], val[1::])))
	print(sum(map(lambda x : x[1], val[1::])))
	print()
	print(real_ticks)
	print(sum(real_ticks))

