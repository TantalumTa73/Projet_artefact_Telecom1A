# -*- coding: utf-8 -*-
"""
Ce script ouvre un fenetre qui affiche en temps réel 
l'image capturée par la camera.

Les carrés sont verts si un aruco est détécté, rouge sinon.
Le carré du haut indique le résultat de la détection avec 
conversion en niveau de gris celui du bas, sans conversion 
avant détéction.

Pour modifier le coefficient permettant de calculer la distance, 
présenter l'aruco devant l'écran, entrez la distance à laquelle
vous vous trouvez de la camera et appuyez sur entrée
"""




import time
import cv2
import numpy as np

import pygame
pygame.init()



cam_port=1
t1 = time.time()
t2 = time.time()


#création détecteur
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
corner_input = np.array([])
ids_input = np.array([])


# Fenetre pygame
running = True
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Test camera")

# objets fenetre
rect1 = pygame.Rect(800, 150, 100, 100)
rect2 = pygame.Rect(800, 350, 100, 100)
GREEN = (0, 200, 20)
RED =(200, 0, 0)
color1 = RED
color2 = RED
MIDDLE_FONT = pygame.font.Font(None,28)
texte = "hello"
input_nbr = 0
cst_dist = 19*80

while running:
    t1 = time.time()
    
    #capture image
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()
    
    #convertion en png
    if result is not None:
        cv2.imwrite("image.png", image)
    else:
        running = False
        print("erreur lors de la capture d'image")
        
    
    #affichage image
    screen.fill((0,0,0))
    pygame_image = pygame.image.load("image.png")
    screen.blit(pygame_image, (0,60))
    
    #détection image en niveau de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #conversion en niveau de gris
    corners, ids, rejected = detector.detectMarkers(gray)
    if ids is None:
        color1 = RED
    else:
        color1 = GREEN
        
    #détection image sans niveau de gris
    corners, ids, rejected = detector.detectMarkers(image, corner_input, ids_input)
    if ids is None:
        color2 = RED
        texte = ""
    else:
        color2 = GREEN
        left_top , right_top, left_bottom, right_bottom = corners[0][0]
        largeur = right_top[0] - left_top[0]
        dist = cst_dist/largeur
        texte = " dist : "+ str(int(dist)) + "    largeur : " + str(largeur)
        
    
    pygame.draw.rect(screen, color1, rect1) 
    pygame.draw.rect(screen, color2, rect2) 
    
    
    #affichage texte
    srf_txt = MIDDLE_FONT.render(texte, True, (255,255,255))
    screen.blit(srf_txt, (720, 80))
    
    srf_txt = MIDDLE_FONT.render("input : "+str(input_nbr), True, (255,255,255))
    screen.blit(srf_txt, (700, 500))
    
    pygame.display.flip()
    t2 = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_RETURN:
                #calibrage : on change cst_dist
                if ids is not None and input_nbr!=0:
                    left_top , right_top, left_bottom, right_bottom = corners[0][0]
                    largeur = right_top[0] - left_top[0]
                    cst_dist = largeur*input_nbr
                    input_nbr = 0
                else:
                    print("erreur lors du calibrage")
            elif event.key == pygame.K_0:
                input_nbr = input_nbr*10 + 0
            elif event.key == pygame.K_1:
                input_nbr = input_nbr*10 + 1
            elif event.key == pygame.K_2:
                input_nbr = input_nbr*10 + 2
            elif event.key == pygame.K_3:
                input_nbr = input_nbr*10 + 3
            elif event.key == pygame.K_4:
                input_nbr = input_nbr*10 + 4
            elif event.key == pygame.K_5:
                input_nbr = input_nbr*10 + 5
            elif event.key == pygame.K_6:
                input_nbr = input_nbr*10 + 6
            elif event.key == pygame.K_7:
                input_nbr = input_nbr*10 + 7
            elif event.key == pygame.K_8:
                input_nbr = input_nbr*10 + 8
            elif event.key == pygame.K_9:
                input_nbr = input_nbr*10 + 9
            elif event.key == pygame.K_BACKSPACE:
                input_nbr = input_nbr//10
            
                
pygame.quit()

print("loop duration : ", t2-t1)
# if result is not None:
#     left_top , right_top, left_bottom, right_bottom = corners[0][0]
#     print(left_top , right_top, left_bottom, right_bottom)
#     print(right_top[0] - left_top[0])
  
# # If image will detected without any error, 
# # show result
# if result:
  
#     # showing result, it take frame name and image 
#     # output
#     cv2.imshow("GeeksForGeeks", image)
  
#     # saving image in local storage
#     cv2.imwrite("GeeksForGeeks.png", image)
  
#     # If keyboard interrupt occurs, destroy image 
#     # window
#     cv2.waitKey(0)
#     cv2.destroyWindow("GeeksForGeeks")
  
# # If captured image is corrupted, moving to else part
# else:
#     print("No image detected. Please! try again")