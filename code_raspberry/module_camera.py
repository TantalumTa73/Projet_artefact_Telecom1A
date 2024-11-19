# -*- coding: utf-8 -*-
"""
Ce module permet d'interagir avec la caméra
"""

import cv2
import os 

#outils de detection de aruco

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

def connect():
    return cv2.VideoCapture('/dev/video0',cv2.CAP_V4L2)

def check_camera_status(cam,verbose=False):
    if not cam.isOpened():
        if verbose:
            print("Camera not opened")
        return False
    if not cam.grab():
        if verbose:
            print("Camera can't grab")
        return False
    if verbose:
        print("Camera working")
    return True


def get_id_aruco(cam):
    """renvoie l'id du premier aruco détecté, -1 si aucun n'est détécté"""
    try :
        result, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #conversion en niveau de gris
        corners, ids, rejected = detector.detectMarkers(gray)
        if ids is not None:
            return ids[0][0]
        return -1


    except :
        #print("erreur lors de la capture d'image")
        return -1

def check_aruco(cam):
    """renvoie True si au moins un aruco est détecté, False sinon"""
    try :
        result, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #conversion en niveau de gris
        corners, ids, rejected = detector.detectMarkers(gray)
        if ids is not None:
            return True 
        return False


    except :
        #print("erreur lors de la capture d'image")
        return False
    return get_id_aruco() != -1

def get_image(cam):
    """capture une image de la camera en la renvoi"""

    result, image = cam.read()
    if result:
        return image
    else:
        print("Image non capturée")

def save_image(image):
    """sauvegarde l'image dans le fichier 'image.png'
    Return 0 s'il n'y a pas eu d'erreur, 1 sinon"""

    #convertion en png
    if not cv2.imwrite(os.path.dirname(os.path.realpath(__file__))+"/static/image.png", image):
        print("writing image failed")
        return 1
    return 0
