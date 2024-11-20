"""Ce module permet d'effectuer des opérations basiques sur 
des vecteurs 2d"""

from math import sqrt, radians, degrees, tan, atan, acos, cos, sin



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

def norme(u):
    """renvoie la norme de u"""
    x, y = u
    return sqrt(x*x + y*y)

def normalize(u):
    """renvoie le vecteur u normalize"""
    x, y = u 
    n = norme(u)
    if n!=0:
        return (x/n, y/n)
    assert False, "on ne peut pas normaliser le vecteur nul"

def mult_scalar(l, u):
    """renvoie u multiplié par le scalaire l"""
    x,y = u 
    return (l*x, l*y)

def add_vect(u, v):
    """renvoie la somme des deux vecteurs"""
    x,y = u 
    a,b = v 
    return (x+a, y+b)

def sub_vect(u, v):
    """renvoie u-v"""
    x,y = u 
    a,b = v 
    return (x-a, y-b)


def rotate_vect(u, deg):
    """tourne le vecteur u de deg degrés dans le sens horaire"""
    x,y = u
    v = (y, -x) #u rotate de pi dans le sens horaire
    alpha = radians(deg)
    return add_vect(mult_scalar(cos(alpha), u), mult_scalar(sin(alpha), v))

def test_rotate_vect():
    assert vect_equal(rotate_vect(rotate_vect((0,1), 90), -90), (0,1))
    assert vect_equal(rotate_vect((0,1), 90), (1,0))


def angle_vect(u,v):
    """renvoie l'angle entre u et v en degrés
    hypothèses : u et v sont normalisés"""
    x,y = u 
    a,b = v 
    prod_scal = x*a + y*b
    alpha = acos(prod_scal)
    prod_vect_z = x*b -y*a 
    if prod_vect_z >= 0 :
        return degrees(-alpha)
    else:
        return degrees(alpha)

def test_angle_vect():
    assert float_equal(angle_vect((0, 1), (1, 0)), 90.0), "erreur tet_angle_vect (1)"
    assert float_equal(angle_vect((0, 1), (-1, 0)), -90.0), "erreur tet_angle_vect (2)"
    assert float_equal(angle_vect((1, 0), (0, 1)), -90.0), "erreur tet_angle_vect (3)"
    assert float_equal(angle_vect((0, 1), (1/sqrt(2), 1/sqrt(2))), 45.0), "erreur tet_angle_vect (4)"

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

if __name__ == '__main__':
    test_rotate_vect()