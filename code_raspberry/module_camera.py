# -*- coding: utf-8 -*-
"""
Ce module permet d'interagir avec la caméra
"""


# -*- coding: utf-8 -*-
"""
Ce module permet d'interagir avec la caméra
"""

import cv2
cam_port=-1

#outils de detection de aruco

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

def connect():
    return cv2.VideoCapture(cam_port)

def check_connexion(cam):
    """renvoie True si la caméra est connecté, False sinon"""
    # for cam_port_test in [0, 5]:
    #     try :
    #         cam = cv2.VideoCapture(cam_port_test)
    #         result, image = cam.read()
    #         if result:
    #             print("cam_port_test = {}".format(cam_port_test))
    #             return result
    #     except :
    #         #print("erreur lors de la capture d'image")
    #         return False
    try :
        result, image = cam.read()
        if result:
            return result
    except :
        #print("erreur lors de la capture d'image")
        return False
    return False

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

def save_image(cam):
    """sauvegarde l'image dans le fichier 'image.png'
    Return 0 s'il n'y a pas eu d'erreur, 1 sinon"""
    try:
        print("had tried to save image")
        result, image = cam.read()
        
        #convertion en png
        if result is not None:
            print("essaye d'écrire l'image dans image.png")
            cv2.imwrite("static/image.png", image)
            print("image capturée")
        else:
            print("image non capturée")
            return 1
        return 0
    except:
        return 1









