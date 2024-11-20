from position_robot import Position_robot
import analyser_drapeau as anal_d
import analyse_image as anal_i
import module_camera as md

print(anal_d.analyser_drapeau(anal_d.drapeau_proche(anal_i.detect_aruco_markers(md.get_image, Position_robot((25,25),(0,1))
))))