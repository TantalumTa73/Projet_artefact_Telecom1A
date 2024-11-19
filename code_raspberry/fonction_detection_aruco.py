

import cv2
import numpy as np

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


def detect_aruco_markers(cam):
    while True:
        # Capture de l'image
        result, image = cam.read()
        if not result:
            print("Erreur lors de la capture de l'image.")
            break

        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Initialiser le dictionnaire de marqueurs ArUco
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters()

        # Détecter les coins des marqueurs ArUco dans l'image
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

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
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.099, camera_matrix, dist_coeffs)

                # Récupérer les informations de distance et d'angle
                dist_cm, angle_deg = get_marker_info(rvec, tvec)

                # Calculer les coordonnées du centre du marqueur
                c = corners[i][0]
                center_x = np.mean(c[:, 0])
                center_y = np.mean(c[:, 1])

                # Convertir les coordonnées x, y de l'image (en pixels) en coordonnées centrées
                center_x -= image.shape[1] / 2
                center_y = -(center_y - image.shape[0] / 2)  # Y inversé

                # Afficher les informations du marqueur
                print(f"ID: {marker_id}, Distance: {dist_cm:.2f} cm, Angle: {angle_deg:.2f}°, Centre: ({center_x:.2f}, {center_y:.2f})")

            # Afficher l'image avec les marqueurs détectés
            cv2.imshow('Detected ArUco Markers', image_markers)
        
        else:
            print("Aucun marqueur ArUco détecté.")

        # Quitter la boucle avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erreur lors de l'ouverture de la caméra.")
    else:
        detect_aruco_markers(cam)
