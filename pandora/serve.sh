#!/bin/bash
source docker.conf

docker run --name $container \
           -p $serve_port:$guest_port \
           -v $host_sphinx:$guest_sphinx \
           -v $host_videos:$guest_videos \
           -v $host_images:$guest_images \
           --link $db_container:$db_ref \
           --rm -t -i \
           $username/$image \
           bash -c "supervisord; tail -f /var/log/sphinx.log"
