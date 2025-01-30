import moteur
import module_camera
from vecteur_2d import *
import numpy as np
#global orient
#orient = ["nord", "est", "sud", "ouest"] # Donne une correspondance numéro direction

def aller_case(x_dest, y_dest, position_robot):

    """ Envoie le robot sur une case depuis une autre case"""
    
    x_dep, y_dep = position_robot.get_pos()
    distX = x_dest - x_dep
    distY = y_dest - y_dep

    print(f"starting {x_dep} {y_dep} dest {x_dest} {y_dest}")
    delta = 2 

    if abs(distX) < delta:
        #on avance que selon y
        if abs(distY) > delta:
            if distY > 0 :
                moteur.rota_deg(position_robot.get_angle_to_point_cardinal("n"), position_robot)
                moteur.avance_cm(distY, position_robot)
            elif distY <0 :
                moteur.rota_deg(position_robot.get_angle_to_point_cardinal("s"), position_robot)
                moteur.avance_cm(-distY, position_robot)
    elif distX > 0:
        moteur.rota_deg(position_robot.get_angle_to_point_cardinal("e"), position_robot)
        #le robot est orienté vers l'est
        moteur.avance_cm(distX, position_robot)
        if abs(distY) > delta:
            if distY > 0 :
                moteur.rota_deg(-90, position_robot)
                moteur.avance_cm(distY, position_robot)
            elif distY < 0:
                moteur.rota_deg(90, position_robot)
                moteur.avance_cm(-distY, position_robot)
    elif distX < 0 :
        moteur.rota_deg(position_robot.get_angle_to_point_cardinal("o"), position_robot)
        #le robot est orienté vers l'ouest
        moteur.avance_cm(-distX, position_robot)
        if abs(distY) > delta:
            if distY > 0 :
                moteur.rota_deg(90, position_robot)
                moteur.avance_cm(distY, position_robot)
            elif distY < 0:
                moteur.rota_deg(-90, position_robot)
                moteur.avance_cm(-distY, position_robot)

def aller_case_opti_zonion(x_dest, y_dest, position_robot):

    """ Envoie le robot sur une case depuis une autre case mais bien"""
    
    x_dep, y_dep = position_robot.get_pos()
    distX = x_dest - x_dep
    distY = y_dest - y_dep
    hypo = np.sqrt(distX**2 + distY**2)

    print(f"starting {x_dep} {y_dep} dest {x_dest} {y_dest}")
    delta = 25

    if abs(distX) < delta:
        #on avance que selon y mais en corrigeant l'erreur de X
        alpha = np.arctan(abs(distX) / abs(distY))
        if abs(distY) > delta:
            if distY > 0 :
                beta = position_robot.get_angle_to_point_cardinal("n")
                beta = (distX / abs(distX)) * alpha + beta
                moteur.rota_deg(beta, position_robot)
                moteur.avance_cm(hypo, position_robot)
            elif distY <0 :
                beta = position_robot.get_angle_to_point_cardinal("s")
                beta = (-distX / abs(distX)) * alpha + beta
                moteur.rota_deg(beta, position_robot)
                moteur.avance_cm(hypo, position_robot)
    elif distX > 0:
        if abs(distY) > delta:
            moteur.rota_deg(position_robot.get_angle_to_point_cardinal("e"), position_robot)
            #le robot est orienté vers l'est
            moteur.avance_cm(distX, position_robot)
            if distY > 0 :
                moteur.rota_deg(-90, position_robot)
                moteur.avance_cm(distY, position_robot)
            elif distY < 0:
                moteur.rota_deg(90, position_robot)
                moteur.avance_cm(-distY, position_robot)
        else:
            alpha = alpha = np.arctan(abs(distY) / abs(distX))
            beta = (-distY / abs(distY)) * alpha + beta
            moteur.rota_deg(beta, position_robot)
            moteur.avance_cm(hypo, position_robot)
    elif distX < 0 :
        if abs(distY) > delta:
            moteur.rota_deg(position_robot.get_angle_to_point_cardinal("o"), position_robot)
            #le robot est orienté vers l'ouest
            moteur.avance_cm(-distX, position_robot)
            if distY > 0 :
                moteur.rota_deg(90, position_robot)
                moteur.avance_cm(distY, position_robot)
            elif distY < 0:
                moteur.rota_deg(-90, position_robot)
                moteur.avance_cm(-distY, position_robot)
        else:
            alpha = alpha = np.arctan(abs(distY) / abs(distX))
            beta = (distY / abs(distY)) * alpha + beta
            moteur.rota_deg(beta, position_robot)
            moteur.avance_cm(hypo, position_robot)

def reperage_rotation(cam):
    """ Tourne sur soi même et prend 16 photos qui sont renvoier avec la position
    du robot au moment ou l'image à été prise"""
    images = [] 
    curr_tick=[0,0]
    for l in range(1,17):
        moteur.rota_petit_angle(l, curr_tick)
        img, res = module_camera.get_image(cam)
        orientation = ((curr_tick[1]*360)/(((2*3.141592*7.85*183.6)-(curr_tick[0]*360)/(2*3.141592*7.85*183.6))/2))
        images.append((img,orientation))
    moteur.reajustement(curr_tick)
    return images


