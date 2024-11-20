
import numpy as np
import module_camera
import moteur
import main
import analyse_image as anal

def drapeau_proche(liste_liste_aru):
    """
    Renvoie la liste d'info de la aruco la plus proche sur une image contenant 
    au moins une aruco
    """
    det_aruco = liste_liste_aru
    d_min = det_aruco[0][1]
    i_min = 0
    for i in range(len(det_aruco)):
        if (det_aruco[i][0] not in [1,2,3,4]) and det_aruco[i][1]< d_min:
            d_min = det_aruco[i][1]
            i_min = i
    
    return det_aruco[i_min]

def analyser_drapeau(liste_aru, position_robot):
    """
    ! cette fonction ne fonctionne que si il y a au moins un drapeau de visible .  
    elle fait se délacer le robot vers la case adjacente au drapeau la plus
    proche du robot. Puis tourne autour du drapeau jusqu'à trouver la face avec 
    l'identifiant puis renvoie l'identifiant
    
    """
    # aller près drapeau
    angle = position_robot.get_angle_orientation()
    x,y = position_robot.get_pos()

    x_drapeau, y_drapeau = liste_aru[5]
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
    angle = position_robot.get_angle_orientation()
    x,y = position_robot.get_pos()
    
    if -45 < angle and angle < 45 :
        orientation = "haut"
    elif -135 < angle and angle < -45 :
        orientation = "gauche"
    elif angle < -135 and angle >135 :
        orientation = "bas"
    else :
        orientation = "droite"
    
    if x_drapeau <x and y_drapeau < y :
        if orientation == "gauche" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
            
    elif x_drapeau >x and y_drapeau < y :
        if orientation == "bas" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
            
    elif x_drapeau <x and y_drapeau > y :
        if orientation == "haut" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
            
    else : 
        if orientation == "droite" :
            ou_est_drapeau = "a_gauche"
        else:
            ou_est_drapeau = "a_droite"
    

    if ou_est_drapeau == "a_gauche":
        for _ in range(4):
            moteur.rota_deg(-45, position_robot)
            aru = drapeau_proche(anal.detect_aruco_markers(module_camera.get_image, position_robot))
            if aru[0] != 0 :
                moteur.rota_deg(45, position_robot)
                return aru[0]
            moteur.rota_deg(45, position_robot)
            moteur.avance_cm(50, position_robot)
            moteur.rota_deg(-90, position_robot)
        return -1
            
    else:
        for _ in range(4):
            moteur.rota_deg(45, position_robot)
            aru = drapeau_proche()
            if aru[0] != 0 :
                moteur.rota_deg(-45, position_robot)
                return aru[0]
            moteur.rota_deg(-45, position_robot)
            moteur.avance_cm(50, position_robot)
            moteur.rota_deg(90, position_robot)
        return -1

    