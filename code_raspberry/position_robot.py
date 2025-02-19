from vecteur_2d import *

class Position_robot:
	def __init__(self, pos_robot, vect_orientation): 
		self.__pos = pos_robot
		self.__vect_orientation = normalize(vect_orientation)
		self.__is_moving = False
		self.__tick_offset = [0, 0]


	### GETTER 

	def get_pos(self):
		return self.__pos


	def get_angle_orientation(self):
		"""retourne l'angle entre le vecteur (0,1) et l'orientation"""
		return angle_vect((0,1), self.__vect_orientation)

	def get_angle_to_point_cardinal(self, pt_cardinal ):
		"""renvoie l'angle à tourner pour être dans une 
		4 directions n, s, e, o"""
		assert pt_cardinal in ['n', 's', 'e', 'o']
		if pt_cardinal=="n":
			return angle_vect(self.__vect_orientation, (0,1))
		elif pt_cardinal=="s":
			return angle_vect(self.__vect_orientation, (0,-1))
		elif pt_cardinal=="e":
			return angle_vect(self.__vect_orientation, (1,0))
		elif pt_cardinal=="o":
			return angle_vect(self.__vect_orientation, (-1,0))

	def is_moving(self):
		return self.__is_moving

	def get_tick_offset(self):
		return self.__tick_offset

	### SETTER

	# /!\ Les fonctions ci-dessous ne doivent être appelées que par moteur.py

	def set_tick_offset(self, tick_off):
		self.__tick_offset = tick_off

	def add_tick_offset(self, tick_off):
		self.__tick_offset[0] += tick_off[0]
		self.__tick_offset[1] += tick_off[1]

	def set_pos(self, x,y):
		self.__pos = (x,y)

	def set_orientation(self, x, y):
		self.__vect_orientation = normalize((x,y))

	def set_angle_orientation(self, angle):
		self.__vect_orientation = rotate_vect((0,1), angle)

	def avancer(self, d):
		"""avance la position de d cm dans la direction donnée par self.__vect_orientation"""
		self.__pos = add_vect(self.__pos, mult_scalar(d, self.__vect_orientation))
		
	def get_moving(self):
		self.__is_moving = True
	
	def stop_moving(self):
		self.__is_moving = False

	def tourner(self, deg):
		"""tourne l'oriantation de deg degrés"""
		self.__vect_orientation = rotate_vect(self.__vect_orientation, deg)




