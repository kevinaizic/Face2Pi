# Face2Pi
Using David Sandberg's [FaceNet tensorflow implementation](https://github.com/davidsandberg/facenet) on a Raspberry Pi 3 with a pre-trained dataset (frozen and optimized to an extent), along with wireless IoT motion detection and onboard camera to provide embedded facial recognition on my roommates' and my faces. The objective is a standalone surveillance system of sorts, automated as much as possible, that emails me pictures of recognized people within an acceptable lag-time.           

Currently there are two ways to use this, one involving pre-training and classifying known faces with facenet's src/classifier.py to "recognize" my roommates and me in this use-case, or what I find a more interesting prospect, the use of facenet's /contributed/cluster.py (with my modifications) to provide *unsupervised* clustering of faces according to a preset Euclidian distance threshold to determine similarity. In both cases my cheese.py or cheese_cluster.py script draws bounding boxes back onto the original images where faces are detected, and these images are emailed to me. Timestamps are used for each image and directory to make debugging and optimization easier, but also to make this feasible as a security application.

Future goals include taking more advantage of facenet providing functionality that logs to a database *when* faces--whether known or not--are seen, as well as consolidating classifier and cluster methods.

I also plan to incorporate a better motion detector so my Pi is less inundated with frivolous disk access and memory consumption when detecting faces (though its current working status is a testament to its performance potential).

Currently a work in progress, take inspiration at your own risk.

# Base Software
- (Raspberry Pi 3) Raspbian stretch lite 2017-11-29             
  * Bazel 0.4.5, used to compile TF with some ARM optimization
  * Python 2.7              
  * mosquitto 1.4.10
  * jpegoptim
  * opencv
- (Workstation) Ubuntu 16.04 LTS                  
  * Python 3.6                   
  * Arduino IDE 1.8.5
- (Both) Tensorflow 1.4.0 (w/ CUDA support on workstation)
  * dependencies                   
