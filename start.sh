#!/bin/bash
source venv/bin/activate;
gnome-terminal --title=Slave1 --tab -- sh -c "./devtools.sh slave"
gnome-terminal --title=Slave2 --tab -- sh -c "./devtools.sh slave"
gnome-terminal --title=Master --tab -- sh -c "./devtools.sh master"
