#!/bin/sh

# export RabbitMQ IP
export mqIP=192.168.50.13

# set hostname 
sudo echo waspmq-backend > /etc/hostname
sudo sed -i "s/127.0.0.1 localhost/127.0.0.1 waspmq-backend/g" /etc/hosts

# install some dependencies
sudo apt-get -y update
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip
sudo apt-get install -y python-pika

# prepare directory 
mkdir -p /usr/local/WASP
cd /usr/local/WASP

# echo "Cloning code and credentials into backend VM"
wget https://raw.githubusercontent.com/laperss/VM-automatic-deploy/master/VM-deploy-scripts/backend.py
wget https://raw.githubusercontent.com/laperss/VM-automatic-deploy/master/VM-deploy-scripts/credentials.txt

echo "Update the server IP adress"
sed -i 's/server=.*/server='$mqIP'/' credentials.txt

sudo apt-get install -y mencoder 
mkdir /home/ubuntu/tmp

