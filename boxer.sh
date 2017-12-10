#!/bin/bash
#gets called by face2pi.sh for using bounding box output to draw bounding boxes on faces in raw/ dir
while IFS='' read -r line || [ -n "$line" ]; do
    python cheese.py $line
done  < "$1"

#to do: also draw name and percent confidence
