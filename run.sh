#!/bin/bash

# build the docker image with "docker build -t snakeskin" in the top-level
# directory
# have XQuartz running before using this script, opened with (open -a XQuartz)
# Then go to XQuartz settings and check "Allow connections from network clients"
# then, to use the container, run "sh run.sh <your command here>",
# such as "sh run.sh nosetests"
# tested on OSX 10.10.5. Requires XQuartz vesion >=2.7.10 (bug in 2.7.9)
xquartz_proc_id=$(ps aux | grep XQuartz | wc -l)

if [ $xquartz_proc_id -lt 0 ]
    then
       open -a XQuartz
fi
ip=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
xhost + $ip
docker run -it --rm -e DISPLAY=$ip:0 -v /tmp/.X11-unix:/tmp/.X11-unix -v `pwd`:/src snakeskin $@

