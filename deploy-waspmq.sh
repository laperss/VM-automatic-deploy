#!/bin/sh
echo 'Set up settings for new VM...'
python3 vmanager.py -c waspmq/waspmq.sh -a create waspmq

echo 'Please wait for the VM to start...'
sleep 45

# Find correct IP adress of the RabbitMQ:
echo 'Set mq IP address'
export mqIP=$(python3 vmanager.py --action show-ip waspmq)

