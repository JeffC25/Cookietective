#!/bin/bash

NUM_CONTAINERS=2
NUM_URLS=4
URLS_PER_CONTAINER=$(( $NUM_URLS/$NUM_CONTAINERS ))

if [[ $# < 1 ]]; then
    echo "Error: no offset specified"
    exit
fi;
INDEX_OFFSET=$1

# build image
docker build -t snickerdoodle ..

for (( i=0 ; i < $NUM_CONTAINERS ; i++ )); do
    UDP_PORT=$(( $i + 9000 ))
    HTTPS_PORT=$(( $i + 9500))

    start=$(( $INDEX_OFFSET + $URLS_PER_CONTAINER*$i ))
    end=$(( $INDEX_OFFSET + $URLS_PER_CONTAINER*($i+1)))
    
    # run container
    docker run -dp $UDP_PORT:53/udp -dp $HTTPS_PORT:8080 --memory="2g" snickerdoodle $start $end

done

