#!/bin/sh

# Install some packages
sudo apt-get -y update
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip

# install python Flask web framework
sudo pip install Flask

#echo "Cloning repo with simcloud"
git clone https://github.com/muyiibidun/WASP.git

#run you code HERE!
cd WASP
python start.py
