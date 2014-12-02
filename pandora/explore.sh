#!/bin/bash
source docker.conf

docker run -p $explore_port:$guest_port \
           --rm -t -i \
           --name $container_explore \
           -v $host_sphinx:$guest_sphinx \
           -v $host_videos:$guest_videos \
           -v $host_images:$guest_images \
           --link $db_container:$db_ref \
           $username/$image \
           bash
