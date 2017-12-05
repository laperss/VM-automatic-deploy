## Automatic VM Deployment
Use Python and NovaStack to automaticly deploy VMs. 

## Instructions
To start a VM, run one of the "deploy-[VM].sh" scripts.

## Dependencies
```bash
$ sudo apt-get update 
$ sudo apt install python-dev python-pip  
$ export LC_ALL=C 
$ sudo pip install python-novaclient==7.1.0 
$ sudo pip install python-swiftclient
```

## Run frontend 
python3 frontend_local.py -c waspmq/credentials_local.txt

## Monitor
python3 monitor.py

## Add backends
./deploy_backend.sh
