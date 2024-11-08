import controller as c

# Moteurs 

moteur = c.Controller()
moteur.set_motor_shutdown_timeout(2)
moteur.standby()

def action_moteur(type_action):

    if type_action[0] == "r":

        dist = int(type_action[1:])
        # CALCUL SAVANT POUR CONVERTIR CENTIMETRE EN TICK
        avance_corrige("left", 1, dist)


def avance_corrige(moteur_princ, ratio, vitesse):

    """ Fait avancer le robot en imposant un ratio (entre 0 et 1) entre les vitesses des moteurs, 
        le moteur le plus rapide est moteur_prin entre left et right """

    if moteur_princ == "left":

        moteur.set_motor_speed(vitesse, ratio * vitesse)
    else:

        moteur.set_motor_speed(ratio * vitesse, vitesse)
