# -*- coding: utf-8 -*-
"""
Ce module permet d'interagir avec la caméra
"""


# -*- coding: utf-8 -*-
"""
Ce module permet d'interagir avec la caméra
"""

try : 

    import cv2
    cam_port=0

    #outils de detection de aruco

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    def check_connexion():
        """renvoie True si la caméra est connecté, False sinon"""
        try :
            cam = cv2.VideoCapture(cam_port)
            result, image = cam.read()
            return result
        except :
            print("erreur lors de la capture d'image")
            return False

    def get_id_aruco():
        """renvoie l'id du premier aruco détecté, -1 si aucun n'est détécté"""
        try :
            cam = cv2.VideoCapture(cam_port)
            result, image = cam.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #conversion en niveau de gris
            corners, ids, rejected = detector.detectMarkers(gray)
            if ids is not None:
                return ids[0][0]
            return -1


        except :
            print("erreur lors de la capture d'image")
            return -1

    def check_aruco():
        """renvoie True si au moins un aruco est détecté, False sinon"""
        try :
            cam = cv2.VideoCapture(cam_port)
            result, image = cam.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #conversion en niveau de gris
            corners, ids, rejected = detector.detectMarkers(gray)
            if ids is not None:
                return True 
            return False


        except :
            print("erreur lors de la capture d'image")
            return False
        return get_id_aruco() != -1

    
    
    if check_connexion():
        print("\nconnexion avec la caméra établie")
    else:
        print("\nproblème de connexion à la caméra")
    

except ModuleNotFoundError:
    print("\nmodule cv2 non trouvé")
    
except:
    print("\nerreur lors de l'ouverture du module")



