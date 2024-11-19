import cv2
cam_port = -1
def save_image():
	"""sauvegarde l'image dans le fichier 'image.png'
	Return 0 s'il n'y a pas eu d'erreur, 1 sinon"""
	print("is about to try to save image")

	cam = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)
	#cam = cv2.VideoCapture(0)

	print(cam.isOpened())
	print(cam.grab())
	print("had tried to save image")

	result, image = cam.read()


	#convertion en png
	if result:
		print("essaye d'écrire l'image dans image.png")
		print(cv2.imwrite("imagenouv.png", image))
		print("image capturée WOHOOOOOO")
	else:
		print("image non capturée")
		return 1

save_image()
