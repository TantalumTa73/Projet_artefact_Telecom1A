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

	real_ticks = 0
	for k in range(0, 11):
		dvitesse = int(k * vitesse / 10) 

		moteur.set_motor_speed(dvitesse, dvitesse)
		real_ticks += dvitesse*time_step*100
		t.sleep(time_step)
	return real_ticks

def acceleration_rota(vitesse, time_step, sens):
	
    """ Accélère de façon progressive jusqu'à une certaine vitesse de rotation """

    if sens == "left":
        mods = (-1, 1)
    else:
        mods = (1, -1)
    vitesse = int(vitesse)

    real_ticks = 0
    for k in range(0, 11):
        dvitesse = int(k * vitesse / 10) 

        moteur.set_motor_speed(int(mods[0] * dvitesse), int(mods[1] * dvitesse))
        real_ticks += dvitesse*time_step*100
        t.sleep(time_step)
    return real_ticks

def deceleration_rota(vitesse, time_step, sens):
	
    """ Décelère de façon progressive jusqu'à l'arrêt de rotation """

    if sens == "left":
        mods = (-1, 1)
    else:
        mods = (1, -1)
    vitesse = int(vitesse)

    real_ticks = 0
    for k in range(0, 11):
        dvitesse = int(k * vitesse / 10) 

        moteur.set_motor_speed(int(mods[0] * (vitesse - dvitesse)), int(mods[1] * (vitesse - dvitesse)))
        real_ticks += (vitesse - dvitesse)*time_step*100
        t.sleep(time_step)
    return real_ticks


def deceleration(vitesse,time_step):

	""" Décélère de façon progressive jusqu'à l'arrêt depuis une certaine vitesse """

	vitesse = int(vitesse)

	real_ticks = 0
	for k in range(0, 11):
		dvitesse = int(k * vitesse / 10)

		moteur.set_motor_speed(vitesse - dvitesse, vitesse - dvitesse)
		real_ticks += (vitesse - dvitesse)*time_step*100
		t.sleep(time_step)
	return real_ticks

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

def rotation_test():
	moteur.set_motor_shutdown_timeout(10)

	# 1,3,30,0.1
	attente, temps_parcours, vitesse, time_step, sens = (1,3,30,0.1, "left") #*sys.argv[1::]

	val = []
	real_ticks = [] 
	
	val.append(moteur.get_encoder_ticks())
	real_ticks.append(acceleration_rota(vitesse,time_step, sens))
	t.sleep(attente)
	val.append(moteur.get_encoder_ticks())
	t.sleep(temps_parcours)
	real_ticks.append(vitesse*temps_parcours*100)
	val.append(moteur.get_encoder_ticks())
	real_ticks.append(deceleration_rota(vitesse,time_step, sens))
	t.sleep(attente)
	val.append(moteur.get_encoder_ticks())

	print(val[1::])
	print(sum(map(lambda x : x[0], val[1::])))
	print(sum(map(lambda x : x[1], val[1::])))
	print()
	print(real_ticks)
	print(sum(real_ticks))
	
def avance_test():
	moteur.set_motor_shutdown_timeout(10)

	# 1,3,30,0.1
	attente, temps_parcours, vitesse, time_step = (1,3,30,0.1) #*sys.argv[1::]

	val = []
	real_ticks = [] 
	
	val.append(moteur.get_encoder_ticks())
	real_ticks.append(acceleration(vitesse,time_step))
	t.sleep(attente)
	val.append(moteur.get_encoder_ticks())
	t.sleep(temps_parcours)
	real_ticks.append(vitesse*temps_parcours*100)
	val.append(moteur.get_encoder_ticks())
	real_ticks.append(deceleration(vitesse,time_step))
	t.sleep(attente)
	val.append(moteur.get_encoder_ticks())

	print(val[1::])
	print(sum(map(lambda x : x[0], val[1::])))
	print(sum(map(lambda x : x[1], val[1::])))
	print()
	print(real_ticks)
	print(sum(real_ticks))

