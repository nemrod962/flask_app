#!/bin/bash
VERSION=$(lsb_release -s -r)
if [ "$VERSION" == '16.04' ]
then
echo "Installing for Ubuntu Xenial from docker repos."
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
INSTALLED=1
else
    if [ "$VERSION" == '18.04' ]
    then
    echo "Installing for Ubuntu Bionic from official repos."
    sudo apt-get install docker.io
    INSTALLED=1
    else
    echo "Ubuntu Release $VERSION not supported."
    fi
fi
if [ -n "$INSTALLED" ]
then
#verify docker
sudo docker run hello-world
fi
