#!/bin/bash
source docker.conf

docker build -t $username/$image .
