#!/bin/sh
export mqIP=`python vmanager.py --action show-ip waspmq`
sed 's/rabbitmq-IP/@mqIP/' waspmq/credentials.txt > waspmq/credentials2.txt
###python vmanager.py -c waspmq/backend.sh -a create waspmq-backend
