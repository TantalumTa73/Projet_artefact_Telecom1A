#!/bin/bash

cd /home/strawberrypi/team1/
source notre_env/bin/activate
cd code_raspberry/
nohup python webpage.py
