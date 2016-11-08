#!/bin/bash
   
data_id=$1 
url_dir=$2

cd HDS_TOOLS/

ret=`python bin/run.py -p 1234567 -d -v 0 -n -i $data_id 2>&1`
#ret="[Download]  output id is [59658],  message: 27, 287, 0,yes"
download_id=`echo $ret |awk -F'[' '{print $3}' |awk -F']' '{print $1}'`

ret=`python bin/run.py -p 1234567 -s -i $download_id 2>&1`
url=`echo $ret |awk -F'"' '{print $4}'`
while [ "$url" != "URL" ]
do
    sleep 3
    ret=`python bin/run.py -p 1234567 -s -i $download_id 2>&1`
    url=`echo $ret |awk -F'"' '{print $4}'`
done
url=`echo $ret |awk -F'"' '{print $6}'`

cd $url_dir
url_1=`echo "$url" | sed 's:\\\/:\/:g'`
wget $url_1 . 
tar_name=`basename $url|awk -F'.tar' '{print $1}'`
tar -xf ${tar_name}.tar
cd $tar_name

for dir in `ls .`
do
    if [ -d $dir ];then
    ls $dir >> ${dir}.list
    fi
done 
cd /home/data/datasystem/model_run

for dir in `ls $url_dir/$tar_name`
do
    if [ -d $url_dir/$tar_name/$dir ];then
        output="$url_dir/$tar_name/${dir}_output"
        mkdir -p $output
        sh shell/run_model.sh surveillance $url_dir/$tar_name/${dir}/ ${url_dir}/$tar_name/${dir}.list $output
        python shell/create_comFormat_from_4class.py ${url_dir}/$tar_name/${dir}.list $output >> $url_dir/$tar_name/label_result.json
    fi 
done


cd HDS_TOOLS/
#ret=`python bin/run.py -p 1234567 -a -i $data_id -f $url_dir/$tar_name/label_result.json -m "upload label_result by cnn predict of surveillance"`

