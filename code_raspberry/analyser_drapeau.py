
import cv2
import numpy as np
import module_camera
import moteur
import main
import position_from_arucos as pfa
import math


def analyser_drapeau(position_robot):
    """
    ! cette fonction ne fonctionne que si il y a au moins un drapeau de visible .  
    elle fait se délacer le robot vers la case adjacente au drapeau la plus
    proche du robot. Puis tourne autour du drapeau jusqu'à trouver la face avec 
    l'identifiant puis renvoie l'identifiant
    
    
    """
    # aller prés drapeau
    angle = position_robot.get_angle_orientation()
    x,y = position.robot.get_pos()

    aru= drapeau_proche()
    distance = aru[1]
    angle_aru =  pfa.get_angle_with_flag(aru)
    angle_absolu_aruco =  angle_aru + angle
    var_x = np.sin(angle_absolu_aruco) * distance 
    var_y = np.cos(angle_absolu_aruco) * distance 
    x_drapeau = x+var_x
    y_drapeau = y+var_y
    x_hd , y_hd = x_drapeau + 25 * 1.41 , y_drapeau + 25 * 1.41
    x_hg , y_hg = x_drapeau - 25 * 1.41 , y_drapeau + 25 * 1.41
    x_bd , y_bd = x_drapeau + 25 * 1.41 , y_drapeau - 25 * 1.41
    x_bg , y_bg = x_drapeau - 25 * 1.41 , y_drapeau - 25 * 1.41
            
    mini = (x-x_hd)**2 +(y-y_hd)**2
    x_min, y_min = x_hd, y_hd
            
    if (x-x_hg)**2 +(y-y_hg)**2 < mini:
        mini = (x-x_hg)**2 +(y-y_hg)**2
        x_min, y_min = x_hg, y_hg
    if (x-x_bd)**2 +(y-y_bd)**2 < mini:
        mini = (x-x_bd)**2 +(y-y_bd)**2
        x_min, y_min = x_bd, y_bd
    if (x-x_bg)**2 +(y-y_bg)**2 < mini:
        mini = (x-x_bg)**2 +(y-y_bg)**2
        x_min, y_min = x_bg, y_bg
         
    main.aller_case(x_min,y_min,position_robot)
    
    
    # tourner autour drapeau
    analyse_drapeau = False
    angle = position_robot.get_angle_orientation()
    x,y = position.robot.get_pos()
    
    if -45 < angle and angle < 45 :
        orientation = "haut"
    elif -135 < angle and angle < -45 :
        orientation = "gauche"
    elif angle < -135 and angle >135 :
        orientation = "bas"
    else :
        orientation = "droite"
    
    
    
    if x_drapeau <x and y_drapeau < y :
        if oritentation == "gauche" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
            
    elif x_drapeau >x and y_drapeau < y :
        if oritentation == "bas" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
            
    elif x_drapeau <x and y_drapeau > y :
        if oritentation == "haut" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
            
    else : 
        if oritentation == "droite" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
    
    
    
    if ou_est_drapeau == "a_gauche":
        while true:
            moteur.rota_deg(-45)
            aru = drapeau_proche()
            if aru[0] != 0 :
                moteur.rota_deg(45)
                return aru[0]
            moteur.rota_deg(45)
            moteur.avance_cm(50)
            moteur.rota_deg(-90)
            
    else:
        while true:
            moteur.rota_deg(45)
            aru = drapeau_proche()
            if aru[0] != 0 :
                moteur.rota_deg(-45)
                return aru[0]
            moteur.rota_deg(-45)
            moteur.avance_cm(50)
            moteur.rota_deg(90)



def drapeau_proche():
    """
    ! cette fonction ne fonctionne que si il y a un drapeau visible 
    celle si renvoie le tableau d'informations associé au drapeau le plus proche
    """
    det_aruco = detect_aruco_markers(module_camera.get_image())
    d_min = det_aruco[0][1]
    i_min = 0
    for i in range(len(det_aruco)):
        if (aru[0] not in [1,2,3,4]) and det_aruco[i][1]< d_min:
            d_min = det_aruco[i][1]
            i_min = i
    
    return det_aruco[i_min]


    
    
    