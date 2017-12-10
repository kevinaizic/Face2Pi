# Face2Pi
Using David Sandberg's [FaceNet tensorflow implementation](https://github.com/davidsandberg/facenet) on a Raspberry Pi 3 with a pre-trained dataset (frozen and optimized to an extent), along with wireless IoT motion detection and onboard camera to provide embedded facial recognition trained on my roommates' and my faces. The objective is a standalone surveillance system of sorts, automated as much as possible, that emails me pictures of recognized people within an acceptable lag-time.           

Future goals include taking more advantage of facenet's ability to compare faces, including scripts that automate the addition and classification of previously unseen faces in order to provide functionality to log *when* faces--whether known or not--are seen.

Currently a work in progress, take inspiration at your own risk.

# Software
-Raspbian stretch lite 2017-11-29
    -Python 3.6
-Ubuntu 16.04 LTS
    -Python 2.7
-Tensorflow 1.4.0
