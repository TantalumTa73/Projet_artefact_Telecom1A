open cv2
cam_port = 0
def save_image():
        """sauvegarde l'image dans le fichier 'image.png'
        Return 0 s'il n'y a pas eu d'erreur, 1 sinon"""
        try:
            print("is about to try to save image")
            cam = cv2.VideoCapture(cam_port)
            print("had tried to save image")
            result, image = cam.read()
            
            #convertion en png
            if result is not None:
                print("essaye d'écrire l'image dans image.png")
                cv2.imwrite("static/image.png", image)
                print("image capturée")
            else:
                print("image non capturée")
                return 1
            return 0
        except:
            return 1