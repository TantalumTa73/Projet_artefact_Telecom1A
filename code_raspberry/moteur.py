import controller as c
import time as t

# Moteurs 

moteur = c.Controller()
moteur.standby()
moteur.set_motor_shutdown_timeout(10)

def action_moteur(type_action):

    if type_action[0] == "r":

        dist = int(type_action[1:])
        # CALCUL SAVANT POUR CONVERTIR CENTIMETRE EN TICK
        avance_corrige("left", 1, dist)

def acceleration(vitesse):

    """ Accélère de façon progressive jusqu'à une certaine vitesse """

    vitesse = int(vitesse)
    for k in range(1, 11):

        moteur.set_motor_speed(int(k * vitesse / 10) , int(k * vitesse / 10))
        t.sleep(0.05)

def deceleration(vitesse):

    """ Décélère de façon progressive jusqu'à l'arrêt depuis une certaine vitesse """

    vitesse = int(vitesse)
    for k in range(1, 11):

        moteur.set_motor_speed(vitesse - int(k * vitesse / 10) ,vitesse - int(k * vitesse / 10))
        t.sleep(0.05)

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
    print(moteur.get_encoder_ticks)
    acceleration(30)
    print(moteur.get_encoder_ticks)
    t.sleep(3)
    print(moteur.get_encoder_ticks)
    deceleration(30)
    print(moteur.get_encoder_ticks)