import moteur
import time as t

# Access the argument from the command line
moteur.avance_cm(107, 0.01, 4)
t.sleep(3)
moteur.avance_cm(-107, 0.01, 4)
