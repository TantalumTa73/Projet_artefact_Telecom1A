import cv2
import numpy as np
import glob

# Dimensions de l'échiquier (nombre de coins intérieurs)
nb_cols = 5  # Nombre de coins intérieurs en largeur
nb_rows = 5  # Nombre de coins intérieurs en hauteur
taille_case = 0.03  # Taille des cases de l'échiquier en mètres

# Préparer les points de l'échiquier dans le système de coordonnées de l'objet (0, 0, 0), (1, 0, 0), ..., (8, 5, 0)
objp = np.zeros((nb_rows * nb_cols, 3), np.float32)
objp[:, :2] = np.mgrid[0:nb_cols, 0:nb_rows].T.reshape(-1, 2)
objp *= taille_case

# Tableaux pour stocker les points d'objets 3D et les points d'images 2D de chaque image
objpoints = []  # Points 3D dans le monde réel
imgpoints = []  # Points 2D dans le plan de l'image

# Lire toutes les images de l'échiquier dans un dossier
images = glob.glob('C:/Users/JOSHUA/.spyder-py3/photos_damier/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Rechercher les coins de l'échiquier
    ret, corners = cv2.findChessboardCorners(gray, (nb_cols, nb_rows), None)

    # Si des coins sont trouvés, les ajouter aux listes de points
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Afficher les coins trouvés (facultatif)
        cv2.drawChessboardCorners(img, (nb_cols, nb_rows), corners, ret)
        cv2.imshow('Coins', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# Calibration de la caméra
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Affichage des résultats de calibration
print("Matrice intrinsèque de la caméra :")
print(mtx)
print("\nCoefficients de distorsion :")
print(dist)