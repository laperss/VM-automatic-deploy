#!/bin/sh
# Find correct IP adress of the RabbitMQ:
export mqIP=`python vmanager.py --action show-ip waspmq`
# Update the credentials
sed -i 's/export mqIP=.*/export mqIP='$mqIP'/' waspmq/frontend.sh
# Create frontend
python3 vmanager.py -c waspmq/frontend.sh -a create waspmq-frontend
