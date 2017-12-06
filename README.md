# Xerces Cloud Application
Course in software development, module on cloud computing. 
The goal is to take input videos and convert them to an output video.
The service must be scaleable and robust.

## Access cloud service
- Private: 
https://129.192.68.4/

## Automatic VM Deployment
We use Python and NovaStack to automaticly deploy VMs. The monitor checks how the resources are being used, and creates/deletes VMs as demanded.  

## Run frontend 
python3 frontend_local.py -c waspmq/credentials_local.txt

## Run the monitor
python3 monitor.py

## Dependencies
```bash
$ sudo apt-get update 
$ sudo apt install python-dev python-pip  
$ export LC_ALL=C 
$ sudo pip install python-novaclient==7.1.0 
$ sudo pip install python-swiftclient
```
