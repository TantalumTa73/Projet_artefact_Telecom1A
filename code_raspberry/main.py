import moteur

global orient
orient = ["nord", "est", "sud", "ouest"] # Donne une correspondance numéro direction

def aller_case(x_dep, y_dep, x_dest, y_dest, orientation):

    """ Envoie le robot sur une case depuis une autre case"""
    
    distX = x_dest - x_dep
    distY = y_dest - y_dep

    if orientation == 0:
        if distY > 0:
            moteur.avance(distY)
        else:
            moteur.avance(-distY)
        if distX > 0:
            moteur.tourne(90)
            moteur.avance(distX)
            return 1
        else:
            moteur.tourne(-90)
            moteur.avance(distX)
            return 3
    elif orientation == 2:
        if distY < 0:
            moteur.avance(distY)
        else:
            moteur.avance(-distY)
        if distX > 0:
            moteur.tourne(-90)
            moteur.avance(distX)
            return 1
        else:
            moteur.tourne(90)
            moteur.avance(distX)
            return 3
    elif orientation == 3:
        if distX < 0:
            moteur.avance(distX)
        else:
            moteur.avance(-distX)
        if distY > 0:
            moteur.tourne(90)
            moteur.avance(distY)
            return 0
        else:
            moteur.tourne(-90)
            moteur.avance(distY)
            return 2
    else:
        if distX > 0:
            moteur.avance(distX)
        else:
            moteur.avance(-distX)
        if distY > 0:
            moteur.tourne(-90)
            moteur.avance(distY)
            return 0
        else:
            moteur.tourne(90)
            moteur.avance(distY)
            return 2