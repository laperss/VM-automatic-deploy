#!/bin/sh
python vmanager.py -c waspmq/waspmq.sh -a create waspmq

# Find correct IP adress of the RabbitMQ:
export mqIP=`python vmanager.py --action show-ip waspmq`
