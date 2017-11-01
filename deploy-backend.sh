#!/bin/sh
# Find correct IP adress of the RabbitMQ:
export mqIP=$(python3 vmanager.py --action show-ip waspmq)
# Update the credentials
sed -i 's/export mqIP=.*/export mqIP='$mqIP'/' waspmq/backend.sh
# Create backend
python3 vmanager.py -c waspmq/backend.sh -a create waspmq-backend
