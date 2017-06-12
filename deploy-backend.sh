#!/bin/sh
# Find correct IP adress of the RabbitMQ:
export mqIP=`python vmanager.py --action show-ip waspmq`
# Update the credentials
sed -i 's/server=.*/server='$mqIP'/' waspmq/credentials.txt
# Create backend
python vmanager.py -c waspmq/backend.sh -a create waspmq-backend
