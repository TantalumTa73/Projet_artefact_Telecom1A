Content of the package
======================


## `webpage.py`

This program manages the server of the webpage. It make the links between the user controls via the webpage and the python modules.


# Motors

## `controller.py`

This file contains a Python module used to interact with the embedded
firmware, for example to set the motor speed, or read the encoders.
Its version must match the one of the embedded firmware.

## `check-wiring.py`

This program checks that the motors are connected as expected by
moving them in turn. Also, it checks that the encoders receive the
right information and appear to be connected correctly.


# Camera

## `module_camera.py`

This module uses the opencv modules to connect the raspberry to the camera. It contains functions to take picture and detect aruco on images.
