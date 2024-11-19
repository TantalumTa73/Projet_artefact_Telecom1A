"""Ce module permet de récupérer la position du robot
grâce aux positions relatives des aruco présents autour de lui"""

import fonction_detection_aruco as detection_aruco
from math import sqrt
import random

dist_to_marker = [None, None, None, None, None] #la première valeur est inutile (id_marker=0 n'existe pas) 
                                                #pour les autres valeurs, None signifie que la distance est inconnue
pos_marker = [None, (0, 350), (150, 350), (150, 50), (0, 50)] #coorodonées en cemtimètres des markers

### UPDATE LA DISTANCE AUX MARKERS

def clear_dist_to_marker():
    """reset dist_to_marker à [None, None, None, None, None]
    (toutes les distances sont inconnues)"""

def set_dist_to_marker(info_images):
    """met à jour la distance aux markers repères
    Argument : liste de 8 listes (une pour chaque orientation du robot) 
    qui contiennent des tuples de la forme (id_marker, dist_marker, angle_marker, pos_on_screen)
    pour chaque aruco détecté sur l'image """
    dists_to_marker = [None, [], [], [], []] # liste des distances mesurées à chaque marker repère.
                                            # on prendra la moyenne
    for info_image in info_images:
        for info_marker in info_image :
            id_marker, dist_marker, angle_marker, pos_on_screen = info_marker
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

def get_markers_connus():
    """return les ids des markers repère dont la distance ets connue"""
    l = []
    for i in range(1, 5):
        if dist_to_marker[i] is not None:
            l.append(i)
    return l

def get_position_from_markers(info_images):
    """renvoie le couple (pos, erreur_distance) qui représente la 
    position du robot en centimètre et l'erreur estimée de la position
    None si la camera n'a pas détecté assez de markers pour déterminer
    sa position
    
    Argument : liste de 8 listes (une pour chaque orientation du robot) 
    qui contiennent des tuples de la forme (id_marker, dist_marker, angle_marker, pos_on_screen)
    pour chaque aruco détecté sur l'image 
    
    Remarque : l'origine (0,0) est tout en bas à gauche de la grille
               les cases font 50 cm de cote
                """
    
    set_dist_to_marker(info_images)

    id_markers = get_markers_connus()
    n = len(id_markers)
    if n<3:
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

def float_equal(x, y):
    """renvoie true si les float different au plus de 0.1""" 
    return abs(x-y)<=0.1

def vect_equal(u, v):
    """renvoie true si les coorodonées different au plus de 0.1""" 
    n = len(u)
    assert len(v) == n, """erreur vect_equal : les vecteurs ne sont pas de la meme taille"""
    for i in range(n):
        if not float_equal(u[i], v[i]):
            return False 
    return True


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
    

if __name__ == '__main__':
    test_set_dist_to_marker()
    test_get_position_from_markers()
    


