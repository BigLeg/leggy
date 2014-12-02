source docker.conf

docker run --name $container \
           -e MYSQL_ROOT_PASSWORD=$mysql_root_passwd \
           -e MYSQL_DATABASE=$mysql_db \
           -p $host_port:$guest_port \
           -d \
           $username/$image
