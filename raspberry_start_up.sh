#!/bin/bash

cd /home/strawberrypi/team1/
git pull
source notre_env/bin/activate
cd code_raspberry/
nohup python webpage.py &
