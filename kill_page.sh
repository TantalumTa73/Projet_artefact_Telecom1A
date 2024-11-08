#!/bin/bash
ps -e | grep python | awk '{ print $1 }' | kill
