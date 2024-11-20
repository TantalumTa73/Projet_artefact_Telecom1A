import moteur

global orient
orient = ["nord", "est", "sud", "ouest"] # Donne une correspondance numéro direction

def aller_case(x_dep, y_dep, x_dest, y_dest, orientation, position_robot):

    """ Envoie le robot sur une case depuis une autre case"""
    
    distX = x_dest - x_dep
    distY = y_dest - y_dep

    if orientation == 0:
        if distY > 0:
            moteur.avance(distY)
        else:
            moteur.avance_cm(-distY,  position_robot)
        if distX > 0:
            moteur.rota_deg(90, position_robot)
            moteur.avance_cm(distX,  position_robot)
            return 1
        else:
            moteur.rota_deg(-90, position_robot)
            moteur.avance_cm(distX,  position_robot)
            return 3
    elif orientation == 2:
        if distY < 0:
            moteur.avance_cm(distY,  position_robot)
        else:
            moteur.avance_cm(-distY,  position_robot)
        if distX > 0:
            moteur.rota_deg(-90, position_robot)
            moteur.avance_cm(distX,  position_robot)
            return 1
        else:
            moteur.rota_deg(90, position_robot)
            moteur.avance_cm(distX,  position_robot)
            return 3
    elif orientation == 3:
        if distX < 0:
            moteur.avance_cm(distX,  position_robot)
        else:
            moteur.avance_cm(-distX,  position_robot)
        if distY > 0:
            moteur.rota_deg(90, position_robot)
            moteur.avance_cm(distY,  position_robot)
            return 0
        else:
            moteur.rota_deg(-90, position_robot)
            moteur.avance_cm(distY,  position_robot)
            return 2
    else:
        if distX > 0:
            moteur.avance_cm(distX,  position_robot)
        else:
            moteur.avance_cm(-distX,  position_robot)
        if distY > 0:
            moteur.rota_deg(-90, position_robot)
            moteur.avance_cm(distY,  position_robot)
            return 0
        else:
            moteur.rota_deg(90, position_robot)
            moteur.avance_cm(distY,  position_robot)
            return 2