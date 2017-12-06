#!/bin/sh

# set hostname 
sudo echo waspmq > /etc/hostname
sudo sed -i "s/127.0.0.1 localhost/127.0.0.1 waspmq/g" /etc/hosts

# Install some packages
sudo apt-get -y update
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip


echo "deb http://www.rabbitmq.com/debian/ testing main"  | sudo tee  /etc/apt/sources.list.d/rabbitmq.list > /dev/null
wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo apt-key add rabbitmq-signing-key-public.asc


apt-key adv --keyserver hkps.pool.sks-keyservers.net --recv-keys 0x6B73A36E6026DFCA

sudo apt-get update
sudo apt-get install rabbitmq-server -y
sudo service rabbitmq-server start
sudo rabbitmq-plugins enable rabbitmq_management
sudo service rabbitmq-server restart

sudo apt-get install -y python-pika

# # create users and set privileges to enable remote connection
rabbitmqctl add_user linnea linnea
 rabbitmqctl set_user_tags linnea administrator
 rabbitmqctl set_permissions -p / linnea ".*" ".*" ".*"


