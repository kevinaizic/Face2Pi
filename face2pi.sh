#!/bin/bash
#called when new faces detected
#makes timestamp directory in datasets folder, copies new images

dir=$(date +%Y-%m-%dx%H_%M_%S)
echo -n $dir > ~/datasets/newestdir.txt

#apparently mkdir -p isn't recommended best practice? 
mkdir ~/datasets/$dir && mkdir ~/datasets/$dir/raw && mkdir ~/datasets/$dir/raw/img 
cp ~/cam/img/*.jpg ~/datasets/$dir/raw/img 
#mv deletes current pics so next time this script doesn't do any repeats
#currently using cp for debugging

export PYTHONPATH=/home/pi/facenet/src #for next step

#detect up to 4 faces per img, takes ~4sec per img plus initialization time
python ~/facenet/src/align/align_dataset_mtcnn.py ~/datasets/$dir/raw ~/datasets/$dir/aligned --image_size 160 --margin 32 --random_order --detect_multiple_faces 4

#if aligned folder empty, no faces were detected (my crappy PIR false triggers a lot) 
if ls -1qA ~/datasets/$dir/aligned/img/ | grep -q .; then ! echo ~~found face/s~~; else  rm -r ~/datasets/$dir && exit 0 ; fi
#delete new img dir and exit if it's empty

#if face(s) detected, run classifier and save output
#############change pkl once trained
python ~/facenet/src/classifier.py CLASSIFY ~/datasets/$dir/aligned ~/facenet/quant/quantized_110547.pb ~/datasets/pi/localsplit.pkl --batch_size 1000 > ~/datasets/$dir/classified.txt

#draw bounding boxes
./boxer.sh ~/datasets/$dir/aligned/bounding*

#to do: optimize face detection, scrounge a resistor and capacitor for a low-pass filter on this junk PIR motion detector
#      -edit confidence thresholds on mtcnn
