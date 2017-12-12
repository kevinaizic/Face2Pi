#!/usr/bin/env python
import time
import picamera
import sys
#import serial
import os
from time import gmtime, strftime
import subprocess

with picamera.PiCamera() as camera:
#   https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
#   camera.sensor_mode = 5 #1640x922 (16:9) (1/10 <= fps <= 40) 2x2 bin
    camera.sensor_mode = 3 #3820x2464 (4:3) (1/10 <= fps <= 15)   
    camera.exposure_mode = "sports" #no motion blur
    camera.resolution = (1640,922) #max
    camera.rotation = 90 #because
#   camera.start_preview() #headless, so no need
    time.sleep(2) #warmup
    camera.brightness = 55 #w/o bathroom light 
#   roundabout handcrafted ring buffer n = 100
#    while True: #frosted kernel flakes
        #I really didn't think I would miss c++
    while True: #frosted debug flakes
        i = 0
        while i < 100: #2 button presses = 100 pictures       
#        time.sleep(.5) #check 
	    #too inaccurate, for now just take ~1 pic every second
	    dash = subprocess.check_output("./dashbutton.py", shell=True)
            if "doritos" in str(dash): #trigger burst of 10 pics on movement (false positives expected)           
                for x in xrange(1,51):
                    name = strftime("%Y-%m-%dx%H_%M_%S") + "(" + str(x) + ")" + '.jpg' #images named by time, cluster folder named by time every 100 images input
	            camera.capture("/home/pi/cam/img/" + name, use_video_port = False)
        	    print(name + " done")
        	    i += 1 #but no regrets
#        	    time.sleep(.5) #allows for ~1 picture per second
	#every 100 pictures send to do clustering
	time.sleep(1) #avoid incomplete image writes
	#run face2pi in background while continuing to fill ring buffer
	subprocess.Popen("/home/pi/cam/script/face2pi_cluster.sh", shell=True)
