
import module_camera
import moteur
import main
import analyse_image 
import analyser_drapeau

def ultime(position_robot,cam):
    image, result = module_camera.get_image(cam)
    liste_aru = analyser_drapeau.drapeau_proche(analyse_image.detect_aruco_markers(image, position_robot))
    moteur.tour_sur_soi_meme()
    # ENVOYER L'ID AU SERV
    id_1,coord_1 = analyser_drapeau.analyser_drapeau(liste_aru,position_robot,cam)
    x1,y1 = coord_1
    x,y = position_robot.get_pos()
    
    x_hd , y_hd = x1 + 25, y1 + 25
    x_hg , y_hg = x1 - 25, y1 + 25
    
    
    if x < x1 :
        main.aller_case(x_hg,y_hg,position_robot)
    else:
        main.aller_case(x_hd, y_hd,position_robot)
    
    angle = position_robot.get_angle_orientation()
    
    if -45 < angle and angle < 45 :
        moteur.rota_deg(-90)
    elif 135 > angle and angle > 45 :
        moteur.rota_deg(180)
    elif angle < -135 and angle >135 :
        moteur.rota_deg(90)
        
    curr_tick = [0,0]
    for i in range(17):
        curr_tick = moteur.rota_petit_angle(l, curr_tick)
        image, result = module_camera.get_image(cam)
        arus = analyse_image.detect_aruco_markers(image, position_robot)
        for j in range(len(arus)):
            if arus[j][0] not in [1,2,3,4]:
                next_flag = arus[j]
                break
    moteur.reajustement(curr_tick)
    id_2,coord_2 = analyser_drapeau.analyser_drapeau(next_flag,position_robot,cam)
    moteur.tour_sur_soi_meme()
    # ENVOYER L'ID AU SERV
    
    
    
    
    
    
    