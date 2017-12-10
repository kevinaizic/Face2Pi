#!/usr/bin/env python
import time
import picamera
import os

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
#   roundabout handcrafted 'ring buffer' with n = 100
    while True: #frosted kernel flakes
        #I really didn't think I would miss c++
        i = 1
        while i < 101:      
            #using ESP8266 and SR501 PIR sensor over MQTT protocol on wifi to detect motion		
            os.system("mosquitto_sub -t outTopic -C 1 > PIR.txt")
            f=open("PIR.txt","r")
            if "SHIT" in f.readline(): #movement: trigger individual pics on movement (false positives expected)           
                name = str(i) + '.jpg'
                camera.capture("/home/pi/cam/img/" + name, use_video_port = False)
                print(name + " done")
                i += 1 #literally zero regrets
	    f.close()
            time.sleep(.5) #possibly unnecessary
            
#todo: optimize to some extent, keep script running somehow...
