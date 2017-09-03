#!/bin/bash

app=slave:app
num_workers=1
ip=0.0.0.0
port=7331

#ip=$1
#port=$2

port=$1

gunicorn --pythonpath . $app --workers=$num_workers -b $ip:$port #&
