#!/bin/bash

python ./launch_listeners.py &
sleep 45
python ./push_to_s3.py &