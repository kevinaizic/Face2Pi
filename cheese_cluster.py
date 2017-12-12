import cv2
import sys
import os

#ensure bounding box exists after reading line from .txt
#take $dir as arg
if len(sys.argv) != 2:
    exit()

dir = "/home/pi/datasets/" + sys.argv[1]
clusters = os.listdir(dir + "/cluster") #0...n
for i in xrange(0, len(clusters)): 
    names = os.listdir(dir + "/cluster/" + str(i))
    for x in xrange(0, len(names)):
        a,b,c,bbs = names[x].split("-") #a,b,c = original timestamp
        xt,yt,xb,yb,num,ext = bbs.split(".") #ext = '.jpg', num = person number in case multiple in original image
        opendir = dir + "/raw/" + a + "-" + b + "-" + c + ".jpg" #path to original picture
	print(opendir)
        img = cv2.imread(opendir,-1)
        cv2.rectangle(img, (int(xt), int(yt)), (int(xb), int(yb)), (255,0,0), 2)
        cv2.imwrite(dir + "/" + str(i) + "_" + a + "-" + b + "-" + c + "_" + num + "_box.jpg",img) #write drawn-over picture to root of timestamp directory
        #new images will all be in root dir regardless of cluster, but cluster name appended to beginning of img name


