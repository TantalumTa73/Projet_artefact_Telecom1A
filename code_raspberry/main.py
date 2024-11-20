import moteur
import module_camera

#global orient
#orient = ["nord", "est", "sud", "ouest"] # Donne une correspondance numéro direction

def aller_case(x_dest, y_dest, position_robot):

    """ Envoie le robot sur une case depuis une autre case"""
    
    x_dep, y_dep = position_robot.get_pos()
    distX = x_dest - x_dep
    distY = y_dest - y_dep

    if distX >0:
        moteur.rota_deg(position_robot.get_angle_to_point_cardinal("e"), position_robot)
        #le robot est orienté vers l'est
        moteur.avance_cm(distX, position_robot)
        if distY > 0 :
            moteur.rota_deg(-90, position_robot)
            moteur.avance_cm(distY, position_robot)
        elif distY < 0:
            moteur.rota_deg(90, position_robot)
            moteur.avance_cm(-distY, position_robot)
    elif distX < 0 :
        moteur.rota_deg(position_robot.get_angle_to_point_cardinal("o"), position_robot)
        #le robot est orienté vers l'ouest
        moteur.avance_cm(-distX, position_robot)
        if distY > 0 :
            moteur.rota_deg(90, position_robot)
            moteur.avance_cm(distY, position_robot)
        elif distY < 0:
            moteur.rota_deg(-90, position_robot)
            moteur.avance_cm(-distY, position_robot)

    else:
        #on avance que selon y
        if distY > 0 :
            moteur.rota_deg(position_robot.get_angle_to_point_cardinal("n"), position_robot)
            moteur.avance_cm(distY, position_robot)
        elif distY <0 :
            moteur.rota_deg(position_robot.get_angle_to_point_cardinal("s"), position_robot)
            moteur.avance_cm(-distY, position_robot)


def reperage_rotation(cam):
    """ Tourne sur soi même et prend 16 photos qui sont renvoier avec la position
    du robot au moment ou l'image à été prise"""
    images = [] 
    curr_tick=[0,0]
    for l in range(1,17):
        moteur.rota_petit_angle(l, curr_tick)
        img, res = module_camera.get_image(cam)
        orientation = ((curr_tick[1]*360)/(2*3.141592*7.85*183.6)-(curr_tick[0]*360)/(2*3.141592*7.85*183.6))
        images.append((img,position_robot.get_pos(),orientation))
    return images


