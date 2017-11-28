#! /usr/bin/python
"""
VM Monitor for starting and closing VMs based on demand. 
"""
from __future__ import print_function
import time
import string
import random
import vmanager


BACKEND_SCRIPT = 'waspmq/backend.sh'
FRONTEND_SCRIPT = 'waspmq/backend.sh'
RABBITMQ_SCRIPT = 'waspmq/waspmq.sh'

NETWORK = 'sw_network'

def id_generator(prefix, size=6):
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(size))
    name = prefix + '_' + name
    return name
    
def get_vms():
    """ Get a dict with all VMs in the network """
    #vms = manager.list()
    vms = {'backend':[], 'frontend':[], 'waspmq':[]}
    for server in manager.nova.servers.list():
        if NETWORK in server.networks:
            if 'backend' in server.name:
                vms['backend'] += [server.networks[NETWORK][0]]
            elif 'frontend' in server.name:
                vms['frontend'] += [server.networks[NETWORK][0]]
            elif 'waspmq' in server.name:
                vms['waspmq'] += [server.networks[NETWORK][0]]
    return vms

# TODO: How to decide which VM to shut down?
def terminate_vm(name):
    """ Terminate a VM """
    manager.terminate(vm=name)

def create_backend():
    """ Start a new VM """
    name = id_generator('backend')
    manager.start_script = BACKEND_SCRIPT
    manager.create(name=name)

def create_frontend():
    """ Start a new VM """
    name = id_generator('frontend')
    manager.start_script = FRONTEND_SCRIPT
    manager.create(name=name)

def create_rabbitmq():
    """ Start a new VM """
    name = id_generator('rabbitmq')
    manager.start_script = RABBITMQ_SCRIPT
    manager.create(name=name)

# TODO: HOW TO MEASURE LOAD? 
def get_load():
    """ Function for estimating the current demands on the application """
    return 0

print("* Start up the manager...")
manager = vmanager.Manager()
print("* Manager is up.")

print("* Search for VMs...")
vms = get_vms()
for vm, ip in vms.items():
    print(vm, ip)

print("* Start monitoring...")
i = 0
try:
    while True:
        i += 1
        
        vms = get_vms()
        if i == 2:
            demand = 0
        elif i == 5:
            break
        else: 
            demand = get_load()

        if demand > 0:
            create_backend()
        elif demand < 0 and len(vms['backend'] >= 1):
            terminate_vm()

        time.sleep(1)

except KeyboardInterrupt:
    print('Shutting down VM monitor...')
