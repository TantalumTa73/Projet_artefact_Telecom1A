from vecteur_2d import *

class Position_robot:
	def __init__(self, pos_robot, vect_orientation): 
		self.__pos = pos_robot
		self.__vect_orientation = normalize(vect_orientation)
		self.__is_moving = False


	### GETTER 

	def get_pos(self):
		return self.__pos

	def get_angle_orientation(self):
		"""retourne l'angle entre le vecteur (0,1) et l'orientation"""
		return angle_vect((0,1), self.__vect_orientation)

	def is_moving(self):
		return self.__is_moving

	### SETTER

	# /!\ Les fonctions ci-dessous ne doivent être appelées que par moteur.py

	def set_pos(self, x,y):
		self.__pos = (x,y)

	def set_orientation(self, x, y):
		self.__orientation = normalize((x,y))

	def avancer(self, d):
		"""avance la position de d cm dans la direction donnée par self.__vect_orientation"""
		self.__pos = add_vect(self.__pos, mult_scalar(d, self.__vect_orientation))
		
	def get_moving(self):
		self.__is_moving = True
	
	def stop_moving(self):
		self.__is_moving = False

	def tourner(self, deg):
		"""tourne l'oriantation de deg degrés"""
		self.__orientation = rotate_vect(self.__orienatation, deg)




