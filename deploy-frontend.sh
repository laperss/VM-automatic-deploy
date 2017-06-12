#!/bin/sh
export mqIP=`python vmanager.py --action show-ip waspmq`
sed -i 's/server=.*/server='$mqIP'/' waspmq/credentials.txt
python vmanager.py -c waspmq/frontend.sh -a create waspmq-frontend
