Content of the package
======================


## `webpage.py`

This program manages the server of the webpage. It make the links between the user controls via the webpage and the python modules.




# Motors

## `controller.py`

This file contains a Python module used to interact with the embedded
firmware, for example to set the motor speed, or read the encoders.
Its version must match the one of the embedded firmware.

## `moteur.py`

This module contains functions to advance or rotate the robot. The other programms have to use only this module to move the robot.

## `moteur_rota.py`

useless ????

## `kill_motors.py`

This program stop the motors. It is not used by webpage.py but can be used by a user manually to stop the robot.





# Camera

## `module_camera.py`

This module uses the opencv modules to connect the raspberry to the camera. It contains functions to take picture and save images on the raspberry.

## `vecteur_2d.py`

This module contains basic functions to use 2d vectors (which are represented by couples).

## `analyse_image.py`

This module contains functions to detect arucos on a picture and get information about them (position, rotation, id, etc.).

## `analyse_drapeau.py`

This module contains a function to get the nearer aruco on a picture and another function to move the robot toward the flag and go around it to find its id.

## `position_from_arucos.py`

This module enables the robot to know its position and its orientation from arucos it detects on pictures.




# Position

## `position_robot.py`

This file contains a python class which is used to represents the position of the robot and its status (is it moving or not, do have motors to correct its position ?). A single instance of this class is created in webpage.py. The other programms have to use a method of this instance to update the position of the robot every time they move the robot. The user also has to set the initial position of the robot when he puts it on the grid.
 
 
 
 
# Algorithms

## `main.py`

This module contains a function to go to a specific cell.

## `fonction_ultime_etape_2.py`

This file contains a function to send the robot to catch the flags during the évaluation intermédiaire.




# Tests

## `check-wiring.py`

This program checks that the motors are connected as expected by
moving them in turn. Also, it checks that the encoders receive the
right information and appear to be connected correctly.

## `test_moteur.py`

This program tests the motors. (useless ????)

## `test_rota.py`

This program tests the motors. (useless ????)

## `test_drap.py`

This file tests the analyser_drapeau.py module.

