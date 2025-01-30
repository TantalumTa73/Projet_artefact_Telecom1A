
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:43:58 2024

@author: JOSHUA
"""

import cv2
import numpy as np
import position_from_arucos as pfa
from math import *

def get_marker_info(rvec, tvec):
    # Distance en utilisant la norme du vecteur de translation
    dist = np.linalg.norm(tvec)  # Distance en mètres
    dist_cm = dist * 100  # Conversion en centimètres

    # Convertir le vecteur de rotation en une matrice de rotation
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    
    # Calculer l'angle autour de l'axe y (en utilisant l'élément [2, 0] de la matrice de rotation)
    # Quand le marqueur est face à la caméra, angle = 0
    angle_rad = np.arctan2(-rotation_matrix[0, 2], rotation_matrix[2, 2])
    if angle_rad < 0:
        angle_deg = -(180 + np.degrees(angle_rad))  # Conversion en degrés
    else:
        angle_deg = 180 - np.degrees(angle_rad)

    return dist_cm, angle_deg

def position_drapeau(liste_aru, position_robot):

    """ Détermine la position d'un drapeau sur la grille en fonction
        de la liste d'info d'une aruco et de la position du robot """

    angle = position_robot.get_angle_orientation()
    x,y = position_robot.get_pos()

    distance = liste_aru[1]
    angle_aru =  pfa.get_angle_with_drapeau(liste_aru)
    angle_absolu_aruco =  angle_aru + angle
    var_x = np.sin(radians(angle_absolu_aruco)) * distance 
    var_y = np.cos(radians(angle_absolu_aruco)) * distance 
    x_drapeau = (x+var_x)
    y_drapeau = (y+var_y)

    return (x_drapeau, y_drapeau)

def rotatoin_drapeau(liste_aru, position_robot):

    angle = position_robot.get_angle_orientation()
    x,y = position_robot.get_pos()

    distance = liste_aru[1]
    angle_aru =  pfa.get_angle_with_drapeau(liste_aru)
    angle_absolu_aruco =  angle_aru + angle

    return angle_absolu_aruco


def detect_aruco_markers(image, position_robot):
    """
    entrée: image sous format numpy array
    sortie : liste de tableau 
            de la forme
            tableau [id,distance en bcm, angle en degré, coordonée du centre du marqueur
                      par rapport au centre de l'image, un tuple des coordonées du drapeau]
            pour chaque aruco détéctée .
            
    """
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialiser le dictionnaire de marqueurs ArUco
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()

    # Détecter les coins des marqueurs ArUco dans l'image
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    liste_retour = []
    # Si des marqueurs ont été détectés
    if ids is not None and len(corners) > 0:
        
        # Dessiner les marqueurs détectés
        image_markers = cv2.aruco.drawDetectedMarkers(image, corners, ids)

        # Matrice intrinsèque de la caméra et coefficients de distorsion
        camera_matrix = np.array([[1.25123380e+03, 0.00000000e+00, 3.66341251e+02],
                                      [0.00000000e+00, 1.25849531e+03, 2.64912740e+02],
                                      [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype=np.float32)
        dist_coeffs = np.array([[-5.48988879e-02, 1.13913226e+01, -1.03279136e-02, 1.58012627e-02,
                                      -1.59207518e+02]], dtype=np.float32)

        # Estimer la pose des marqueurs détectés
        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in [1,2,3,4]:
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.1, camera_matrix, dist_coeffs)
            else:
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, camera_matrix, dist_coeffs)
            #print("marker : ", marker_id, "rvec : ", rvec)
            # Récupérer les informations de distance et d'angle
            dist_cm, angle_deg = get_marker_info(rvec, tvec)

            # Calculer les coordonnées du centre du marqueur
            c = corners[i][0]
            center_x = np.mean(c[:, 0])
            center_y = np.mean(c[:, 1])

            # Convertir les coordonnées x, y de l'image (en pixels) en coordonnées centrées
            center_x -= image.shape[1] / 2
            center_y = -(center_y - image.shape[0] / 2)  # Y inversé
            centre = (center_x,center_y)

            # Afficher les informations du marqueur
            liste_retour.append([marker_id, dist_cm,angle_deg,centre,None])
            pos_drap = position_drapeau(liste_retour[-1], position_robot)
            liste_retour[-1][-1]= pos_drap
    return liste_retour
        
