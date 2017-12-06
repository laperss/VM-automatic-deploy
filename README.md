# Xerces Cloud Application
This is a cloud application for robust video conversion. The application takes input videos and convert them to output videos of lower quality. For scalability and robustness, the cloud service scales with usage and is robust to backend failures.

## Run application 
```
python3 frontend_local.py -c waspmq/credentials_local.txt
python3 monitor.py
```

### Dependencies
```bash
$ sudo apt-get update 
$ sudo apt install python-dev python-pip  
$ export LC_ALL=C 
$ sudo pip install python-novaclient==7.1.0 
$ sudo pip install python-swiftclient
```
## Architecture
The different components of the system are designed in a modular fashion, where each component has a specified task. The different components in the system are discussed below.

### Rabbitmq

### Backends

### Load Generator (clients.py)
To simulate a realistic load and to test the scaling of the system a load generator is used. The load generator perodically increases and decreases the number of convertion requests per minute.

### Monitor (vmonitor.py)
The monitor is responsible for managing the amount of backend VMs in the system. It monitors the load of the system through the cpu usage of each VM, and automatically creates or deletes VMs depending on the demand. Openstack nova is used for the automatic deployment of VMs. In order to avoid the rapid creation and deletion of VMs an averaging window is used, during which the cpu usage is measured multiple times. If all VMs are fully loaded, a new VM will be created. If one of the VMs is not used this VM will be terminated. After every change in the system, a timer is used to make sure that the system has time to respond to the change.
