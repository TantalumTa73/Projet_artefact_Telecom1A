#!/bin/bash
kill $(ps -e | grep python | awk '{ print $1 }')
