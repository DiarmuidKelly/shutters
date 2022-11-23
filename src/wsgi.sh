#! /usr/bin/bash

export PATH="/home/pi/.local/bin:$PATH"
echo $(which python3)
uwsgi --ini /opt/shutters/project.ini
