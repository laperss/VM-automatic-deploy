# Xerces Cloud Application
This is a cloud application for robust video conversion. The application takes input videos and convert them to output videos of desired format. For scalability and robustness, the cloud service scales with usage. 

The cloud service is managed from: https://129.192.68.4/

We use Python and [Openstack nova](https://docs.openstack.org/nova/pike/) for automatic deployment of VMs. 
This is done from the [monitor](vmonitor.py) checks how the resources are being used, and creates/deletes VMs as demanded. 

### Run application 
```
python3 frontend_local.py -c waspmq/credentials_local.txt
python3 monitor.py
```

## Dependencies
```bash
$ sudo apt-get update 
$ sudo apt install python-dev python-pip  
$ export LC_ALL=C 
$ sudo pip install python-novaclient==7.1.0 
$ sudo pip install python-swiftclient
```
