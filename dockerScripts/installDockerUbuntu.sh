#!/bin/bash
#1 update repos
sudo apt-get update
#2 install dependencies
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
#3 add repo key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#4 add repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
#5 update repos
sudo apt-get update
#6 install docker
sudo apt-get install docker-ce
#verify docker
sudo docker run hello-world
