#! /usr/bin/bash

export PATH="/home/pi/.local/bin:$PATH"
echo $(which python3)
uwsgi /opt/shutters/project.ini