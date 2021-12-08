#!/bin/bash

###############################################################################
# launch.sh script
# simple way to coordinate the 2 python scripts 
# launching  them in backgroud mode with a delay of period*1.5 between them
###############################################################################

python3 ./launch_listeners.py &
sleep 45
python3 ./push_to_s3.py &
