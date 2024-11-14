#!/bin/bash
x=$(ps -e | grep python | awk '{ print $1 }')

if [ ! -z "$x" ]; then 
	kill $(ps -e | grep python | awk '{ print $1 }')
	echo "Page killed successfully"
else 
	echo "Page not running"
fi
