"""Ce module permet de récupérer la position du robot
grâce aux positions relatives des aruco présents autour de lui
Fonction a utiliser : get_position_from_markers """

import fonction_detection_aruco as detection_aruco
from math import sqrt, radians, degrees, tan, atan, acos, cos, sin
import random
from vecteur_2d import *

dist_to_marker = [None, None, None, None, None] #la première valeur est inutile (id_marker=0 n'existe pas) 
                                                #pour les autres valeurs, None signifie que la distance est inconnue
angle_with_marker = [None, None, None, None, None] #les angles sont en degrés
pos_marker = [None, (0, 350), (150, 350), (150, 50), (0, 50)] #coorodonées en cemtimètres des markers

largeur_image = 640
hauteur_image = 480
angle_vue = 28 #degrés
dist_foyer_ecran = (largeur_image//2)/tan(radians(angle_vue/2))
dist_camera_centre = 6


### CHANGER LA POSITION DES MARKERS

def set_pos_marker(list_pos:list):
    """change les positions des markers
    list_pos est une liste de 4 positions (x,y) des markers"""
    assert len(list_pos)==4
    for i in range(4):
        assert(len(list_pos[i])==2)
        pos_marker[i+1] = list_pos[i]


### UPDATE LA DISTANCE AUX MARKERS

def clear_dist_to_marker():
    """reset dist_to_marker à [None, None, None, None, None]
    (toutes les distances sont inconnues)"""

def get_dist_from_center(dist_marker, pos_on_screen):
    """renvoie la distance du centre du robot au marker"""

def set_dist_to_marker(info_images):
    """met à jour la distance aux markers repères
    Argument : liste de 8 listes (une pour chaque orientation du robot) 
    qui contiennent des tuples de la forme (id_marker, dist_marker, angle_marker, pos_on_screen)
    pour chaque aruco détecté sur l'image """
    dists_to_marker = [None, [], [], [], []] # liste des distances mesurées à chaque marker repère.
                                            # on prendra la moyenne
    for info_image in info_images:
        for info_marker in info_image :
            id_marker, dist_marker, angle_marker, pos_on_screen, _ = info_marker
            if 1<= id_marker and id_marker <=4:
                dists_to_marker[id_marker].append(dist_marker)
    clear_dist_to_marker()
    for id_marker in range(1, 5):
        n = len(dists_to_marker[id_marker])
        if n!=0:
            #on enregistre la moyenn des distances
            s = 0
            for dist in dists_to_marker[id_marker]:
                s += dist
            dist_to_marker[id_marker] = s/n

def test_set_dist_to_marker():
    info_images = [[], [], [], [], [], [], [], []]
    info_images[3] = [(1, 5, 0, (0,0)), (2, 10, 5, (0,0))]
    info_images[4] = [(2, 10, 0, (0,0)), (1, 5, -5, (0,0)), (5, 50, 30, (0,0))]
    info_images[5] = [(5, 55, 20, (0,0))]

    set_dist_to_marker([[], [], [], [], [], [], [], []])
    assert dist_to_marker == [None, None, None, None, None], "erreur test_set_dist_to_marker (1)"
    set_dist_to_marker(info_images)
    assert dist_to_marker == [None, 5, 10, None, None], "erreur test_set_dist_to_marker (2)"



### DETERMINER LA POSITION

def get_sommet(pt_a, pt_b, ac, bc):
    """renvoie la liste des sommets c possibles d'un
    triangle abc en fonction des points a, b et des longueurs
    ac et bc.
    Remarque, la liste revoyée est de taille 0 ou 2 (eventuellement 2 fois la meme poition)"""
   
    xa, ya = pt_a
    xb, yb = pt_b
    d=sqrt((xb-xa)**2+(yb-ya)**2)
   
    if (xa==xb and ya==yb): #points confondus
        #print("pas de solution possible, points confondus")
        return []
    if (d > ac + bc) : #points trop éloignés
        #print("pas de solution possible, points trop éloignés")
        return []
    if d < abs(ac - bc): # points trop raprochés
        #print("pas de solution possible, points trop proches")
        return []
    else:
        a=(bc**2-(ac**2)+d**2)/(2*d)
        h=sqrt(bc**2-a**2)
   
   
        xh = xb + (a/d)*(xa - xb)
        yh = yb + (a/d)*(ya - yb)
        if (xh - xb)**2 + (yh-yb)**2>0:
            norme = sqrt((xh - xb)**2 + (yh-yb)**2)
            vectx1 = (- (yh - yb)/norme )*h # sens trigo
            vecty1 = (+ (xh - xb)/norme)*h
           
            vectx2 = (+ (yh - yb)/norme )*h # sens pas trigo
            vecty2 = (- (xh - xb)/norme)*h
           
            xc1 = xh + vectx1
            yc1 = yh + vecty1
           
            xc2 = xh + vectx2
            yc2 = yh + vecty2
           
            return [(xc1, yc1), (xc2, yc2)]
            
        else :
            #print("pas de solution")
            return []

def get_dist(pt_a, pt_b):
    """renvoie la dist entre A et B"""
    xa, ya = pt_a
    xb, yb = pt_b
    return sqrt((xb-xa)**2+(yb-ya)**2)

def get_markers_dist_connus():
    """return les ids des markers repère dont la distance est connue"""
    l = []
    for i in range(1, 5):
        if dist_to_marker[i] is not None:
            l.append(i)
    return l

def get_markers_angle_connus():
    """return les ids des markers repère dont l'angle est connu"""
    l = []
    for i in range(1, 5):
        if angle_with_marker[i] is not None:
            l.append(i)
    return l

def get_dist_to_terrain(pos_robot):
    """renvoie la distance au terrain"""
    # max_x = 150
    # max_y = 350
    # x, y = pos_robot 
    # if x>=0 and x<=max_x:
    #     if y>=0 and y<=max_y :
    #         return 0 
    #     if y<0 :
    #         return -y 
    #     else:
    #         #y>max_y 
    #         return y - max_y
    # elif y>=0 and y<=max_y:
    #     if x<0 :
    #         return -x
    #     else:
    #         #x>max_x 
    #         return x - max_x
    # else: 
    #     coins = [(0,0), (0,150), (350, 0), (350, 150)]
    #     dist_coins = [] 
    #     for i in range(4):
    #         dist_coins.append(norme(sub(coins[i], pos_robot)))
    #     min_dist = dist_coins[0]
    #     for i in range(1, 4):
    #         if dist_coins[i]<min_dist:
    #             min_dist = dist_coins[i]
    #     return min_dist
    max_x = 150
    max_y = 350
    x, y = pos_robot 
    coord = [x,y]
    coord_max = [max_x,max_y]
    coord_prime = [0,0]
    for i in [0,1]:
        if coord[i] <= 0:
            coord_prime[i] = 0
        elif 0 < coord[i] <= coord_max[i]:
            coord_prime[i] = coord[i] 
        else:
            coord_prime[i] = coord_max[i]

    return norme(sub_vect(coord,coord_prime))

        

def get_position_from_markers(info_images):
    """renvoie le couple (pos, erreur_distance) qui représente la 
    position du robot en centimètre et l'erreur estimée de la position
    None si la camera n'a pas détecté assez de markers pour déterminer
    sa position
    
    Argument : liste de listes (une pour chaque orientation du robot) 
    qui contiennent des tuples de la forme (id_marker, dist_marker, angle_marker, pos_on_screen)
    pour chaque aruco détecté sur l'image 
    
    Remarque : l'origine (0,0) est tout en bas à gauche de la grille
               les cases font 50 cm de cote
                """
    
    set_dist_to_marker(info_images)

    id_markers = get_markers_dist_connus()
    n = len(id_markers)
    if n<2:
        print(f"get_position_from_arucos : {n} markers repères détectés n'est pas suffisant pour déterminer la position")
        return None

    

    pt_a = pos_marker[id_markers[0]] #1er marker détecté
    pt_b = pos_marker[id_markers[1]] #2eme marker détecté
    ac = dist_to_marker[id_markers[0]]
    bc = dist_to_marker[id_markers[1]]
    pos_possibles = get_sommet(pt_a, pt_b, ac, bc)
    if pos_possibles == []:
        print("get_position_from_arucos : aucune position possible trouvée avec la triangulation")
        return None 
    elif len(pos_possibles) == 2:

        if n==2 : 
            #deux positions possibles, on doit choisir la plus logique
            dist_0 = get_dist_to_terrain(pos_possibles[0])
            dist_1 = get_dist_to_terrain(pos_possibles[1])
            if dist_0<dist_1:
                return pos_possibles[0], (norme(sub_vect(pos_possibles[0], pos_possibles[1])))
            return pos_possibles[1], (norme(sub_vect(pos_possibles[0], pos_possibles[1])))
        elif n>=3 : 

            #on a deux positions possibles. On les départage avec un troisieme marker
            id_marker = id_markers[2]
            #on regarde la difference entre la distance entre les positions possibles et le troisieme marker
            #et la distance réelle entre le robot et le troisieme marker
            diff_dist_0 = abs(get_dist(pos_possibles[0], pos_marker[id_marker]) - dist_to_marker[id_marker]) 
            diff_dist_1 = abs(get_dist(pos_possibles[1], pos_marker[id_marker]) - dist_to_marker[id_marker]) 
            if diff_dist_0 < diff_dist_1:
                erreur_distance = diff_dist_0
                pos = pos_possibles[0]
            else:
                erreur_distance = diff_dist_1
                pos = pos_possibles[1]
            if n == 4:
                # on vérifie la position avec le 4eme marker 
                id_marker = id_markers[2]
                diff_dist = abs(get_dist(pos, pos_marker[id_marker]) - dist_to_marker[id_marker]) 
                erreur_distance = max(erreur_distance, diff_dist)
            return (pos, erreur_distance)

    else:
        assert False, "get_position_from_arucos : erreur lors de la triangulation"



def test_get_position_from_markers():
    erreur_flottant = 0.1
    for i in range(100):
        x = random.random()*150
        y = random.random()*350
        pos_robot = (x, y)
        info_images = [[], [], [], [], [], [], [], []]
        for id_marker in range(1, 5):
            info_images[0].append((id_marker, get_dist(pos_marker[id_marker], pos_robot), 0, (0,0)))
        (pos, erreur_distance) = get_position_from_markers(info_images)
        assert vect_equal(pos, pos_robot), "erreur test_get_position_from_marker : position incorrecte"
        assert float_equal(erreur_distance, 0.0), "erreur test_get_position_from_marker : erreur_distance non nulle"


### ORIENTATION





def get_angle_from_pos_on_screen(pos_on_screen):
    """renvoie l'angle en degrés entre la direction vers 
    laquelle regarde la caméra et un objet qui se trouve 
    à la position pos_on_screen sur l'image en pixel"""
    x, y = pos_on_screen 
    alpha = atan(x/dist_foyer_ecran)
    return degrees(alpha)



def vect_mean(directions:list):
    """renvoie la 'moyenne' des vecteurs et le plus grand écart d'angle entre eux
    hypothèses : tous les vecteurs sont normalises"""
    n = len(directions)
    if n<1:
        return None
    angles = [0] #angles par rapport à direction[0]
    for i in range(1, n):
        angles.append(angle_vect(directions[0], directions[i]))
    s = 0
    min_angle = 0
    max_angle = 0
    for i in range(n):
        s+= angles[i]
        if angles[i]>max_angle :
            max_angle = angles[i]
        if angles[i]<min_angle : 
            min_angle = angles[i]
    angle = s/(n) #moyenne des angles 
    return rotate_vect(directions[0], angle), (max_angle-min_angle)

def test_vect_mean():
    direction, ecart_angle = vect_mean([(0,1), (0,1), (0,1)])
    assert vect_equal(direction, (0,1)), "erreur test_vect_mean (1)"
    assert float_equal(ecart_angle, 0.0), "erreur test_vect_mean (2)"
    direction, ecart_angle = vect_mean([(1,0)])
    assert vect_equal(direction, (1,0)), "erreur test_vect_mean (3)"
    assert float_equal(ecart_angle, 0.0), "erreur test_vect_mean (4)"
    direction, ecart_angle = vect_mean([(0,1), (1,0)])
    assert vect_equal(direction, (1/sqrt(2),1/sqrt(2))), "erreur test_vect_mean (5)"
    assert float_equal(ecart_angle, 90.0), "erreur test_vect_mean (6)"

    

def get_orientation(pos_robot, info_image):
    """renvoie le vecteur unitaire orientation qui indique la direction pointée par la caméra
    ainsi qu'une erreur en degrés
    renvoie None si aucun aruco n'est sur l'image
    Argument : 
        - la position en centimètres du robot
        - liste de tuples de la forme (id_marker, dist_marker, angle_marker, pos_on_screen)"""
    for (id_marker, dist_marker, angle_marker, pos_on_screen,_) in info_image :
        if 1<=id_marker and id_marker <=4:
            angle_with_marker[id_marker] = get_angle_from_pos_on_screen(pos_on_screen)
    id_markers = get_markers_angle_connus()
    directions = []
    for id_marker in id_markers:
        u = sub_vect(pos_marker[id_marker], pos_robot)
        directions.append(normalize(rotate_vect(u, angle_with_marker[id_marker])))
    if directions==[]:
        return None
    direction, erreur_angle = vect_mean(directions)
    return direction, erreur_angle
        
def test_get_orientation():
    pos_robot = (50, 250)
    x = dist_foyer_ecran*tan(radians(22.5))
    info_image = [(1, 111.8, None, (x,0))]
    direction, erreur = get_orientation(pos_robot, info_image)
    assert vect_equal(direction, (0,1)), "erreur test_get_orientation (1)"
    assert float_equal(erreur, 0.0), "erreur test_get_orientation (2)"


def get_angle_with_drapeau(info_marker):
    """renvoie l'angle entre l'orientation de la camera et le drapeau"""
    id_marker, dist_marker, angle_marker, pos_on_screen, caca = info_marker
    angle = get_angle_from_pos_on_screen(pos_on_screen)
    return angle




if __name__ == '__main__':
    test_set_dist_to_marker()
    test_get_position_from_markers()
    assert abs(get_angle_from_pos_on_screen((160, 0))-7) <0.5 #~7°
    assert abs(get_angle_from_pos_on_screen((-160, 0))+7) <0.5 #~-7°
    test_angle_vect()
    test_vect_mean()
    test_get_orientation()
    


