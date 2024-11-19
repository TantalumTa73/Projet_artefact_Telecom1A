import controller as c
import time as t

# Moteurs 

moteur = c.Controller()
moteur.standby()

def action_moteur(type_action):

    if type_action[0] == "r":

        dist = int(type_action[1:])
        # CALCUL SAVANT POUR CONVERTIR CENTIMETRE EN TICK
        avance_corrige("left", 1, dist)


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
        moteur.set_motor_speed(vitesse, int(ratio * vitesse))
        t.sleep(2)
        print(moteur.get_encoder_ticks())
    else:

        moteur.set_motor_speed(int(ratio * vitesse), vitesse)

def rotation_test(temps, vitesse, côté):
    if côté == "left":
        vitesse = -vitesse
    moteur.set_motor_shutdown_timeout(2)
    moteur.set_motor_speed(vitesse, -vitesse)
    print(moteur.get_encoder_ticks())
    


