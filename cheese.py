#!/usr/bin/env python
#gets called by boxer.sh (which is called by face2pi.sh), sorry not sorry
import cv2
import sys

#ensure bounding box exists after reading line from .txt which should contain right number of args (including coordinates)
if len(sys.argv) != 6:
    exit()

#open raw img version given aligned path w/ coordinates
a,b,c,d,e,f,g,h = sys.argv[1].split("/")
dir = "/home/pi/datasets/" + e  + "/raw/img/"
i,j = h.split(".")
k,l = i.split("_") #ex 6_0, l -> # people, if > 1

opendir = dir + k + ".jpg" #original picture
xt = int(sys.argv[2])
yt = int(sys.argv[3])
xb = int(sys.argv[4])
yb = int(sys.argv[5])

img = cv2.imread(opendir,-1)
cv2.rectangle(img, (xt, yt), (xb, yb), (255,0,0), 2)
cv2.imwrite(dir + i + "_box.jpg",img)


