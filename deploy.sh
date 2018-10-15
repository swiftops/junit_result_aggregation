#!/bin/bash
export HOST_IP=<hostip>
cd /home/ubuntu/microservice
docker stop <container_name> || true && docker rm <container_name> || true
docker pull <image-name> && docker rmi $(docker images -q -f dangling=true) && docker-compose up -d --remove-orphans
