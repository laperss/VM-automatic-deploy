# Scalable Cloud Video Application
This is a cloud application for robust video conversion. The application takes input videos and convert them to output videos of another size. For scalability and robustness, the cloud service scales with usage and is robust to backend failures.

## Run application 
The application is run from one "master vm". This VM must be accesable from internet via a floating IP. The frontend is started from the frondend folder:
```bash
python3 frontend.py -c credentials.txt
```
The monitor is started using: 
```bash
python3 monitor.py
```

### Dependencies
The following must be done on the master VM before the pakcages can be run: 
```bash
sudo apt-get update 
sudo apt install python-dev python-pip  
export LC_ALL=C 
sudo pip install python-novaclient==7.1.0 
sudo pip install python-swiftclient
```
## Architecture
![Cloud architecture](https://user-images.githubusercontent.com/4593893/33714926-14ec6f1a-db51-11e7-9bcc-9de7c1b4616c.png)

The different components of the system are designed in a modular fashion, where each component has a specified task. The different components in the system are discussed below.

### Rabbitmq
For distribution of the load, we use [RabbitMQ](http://www.rabbitmq.com/) and [Pika](https://pika.readthedocs.io/en/0.10.0/). 
The queue runs on a separate VM called "waspmq". The queue transfers information about the address and name of the video file to be downloaded and transformed. 

### Backends
Every backend is connected to the RabbitMQ. Upon request, the backend will receive a JSON object containing information about the video to be converted. The video must be transfered to the backend from the frontend using ssh. The video is then converted using [MEncoder](https://help.ubuntu.com/community/MEncoder). A JSON object is sent back to the frontend including the link to where the video can be downloaded from. 

### Load Generator ([clients.py](clients.py))
To simulate a realistic load and to test the scaling of the system a load generator is used. The load generator perodically increases and decreases the number of convertion requests per minute.

### Monitor ([vmonitor.py](vmanager.py))
The monitor is responsible for managing the amount of backend VMs in the system. It monitors the load of the system through the cpu usage of each VM, and automatically creates or deletes VMs depending on the demand. Openstack nova is used for the automatic deployment of VMs. In order to avoid the rapid creation and deletion of VMs an averaging window is used, during which the cpu usage is measured multiple times. If all VMs are fully loaded, a new VM will be created. If one of the VMs is not used this VM will be terminated. After every change in the system, a timer is used to make sure that the system has time to respond to the change.

The monitor is also in charge of starting the VMs. This is done using the script [vmanager.py](vmanager.py). When a command is given to start a new VM, it will generate a name for the VM and a startup script for the VM to run upon creation. If the VM is a backend VM, the startup script includes downloading and starting the [backend.py](VM-deploy-scripts/backend.py) script.

## Results
Experiments were run where teh VMs are put through cyclic load changes. The results show that the system is able to adapt to the number of requests, with a slight time delay corresponding to the startup time of the VMs. 

The figure below shows the requests per minute (blue) and the number of VMs that were automatically started (red). 

![Experimental results](https://user-images.githubusercontent.com/4593893/35264087-a467e914-001b-11e8-9c13-a37ecaf3dc6a.png)
