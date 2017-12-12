#called when new faces detected
#makes timestamp directory in datasets folder, copies new images

dir=$(date +%Y-%m-%dx%H_%M_%S)
echo -n $dir > ~/datasets/newestdir.txt
mkdir ~/datasets/$dir && mkdir ~/datasets/$dir/raw && mkdir ~/datasets/$dir/cluster
mv ~/cam/img/*jpg ~/datasets/$dir/raw
#mv deletes current pics so next time this script doesn't do any repeats

#optimize jpgs in raw dir: lossy (75% quality) reduces size by factor of ~10
jpegoptim -m 50 ~/datasets/$dir/raw/*jpg >> ~/datasets/$dir/jpegoptim_output.txt 

export PYTHONPATH=/home/pi/facenet/src #env variable for next step

#minimum 2 similar pics to be considered individual face, threshold euclidean distance <=.85 at worst to be considered "match"
#python ~/facenet/contributed/cluster.py  ~/facenet/quant/quantized_110547.pb ~/datasets/$dir/raw ~/datasets/$dir/cluster --cluster_threshold .85 --min_cluster_size 2 >> ~/datasets/$dir/cluster_output.txt

#removing cluster size min requirement
python ~/facenet/contributed/cluster.py  ~/facenet/quant/quantized_110547.pb ~/datasets/$dir/raw ~/datasets/$dir/cluster --cluster_threshold .85 >> ~/datasets/$dir/cluster_output.txt

#debug
#python ~/facenet/contributed/cluster.py  ~/facenet/quant/quantized_110547.pb ~/datasets/2017-12-11x16_17_05/raw ~/datasets/2017-12-11x16_17_05/cluster --cluster_threshold .85 >> ~/datasets/2017-12-11x16_17_05/cluster_output.txt

#if cluster folder empty, no faces detected (my crappy PIR false triggers a lot) 
if ls -1qA ~/datasets/$dir/cluster | grep -q .; then ! echo ~~found face/s: ~/datasets/$dir~~; else echo deleting ~/datasets/$dir &&  rm -r ~/datasets/$dir && exit 0 ; fi

#draw bounding boxes
python ~/cam/script/cheese_cluster.py $dir 
