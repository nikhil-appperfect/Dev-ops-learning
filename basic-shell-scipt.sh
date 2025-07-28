#!/bin/bash

##################
#Author : Nikhil
#date : 09/07/25
#
# This script output the node health
#version: v1
#####################


# echo "for each command to know what cmd is executed

set -x #debug mode -- first print cmd then execute it

df -h

free -g

nproc
