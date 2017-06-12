## Automatic VM Deployment
Use Python and NovaStack to automaticly deploy VMs. 

## Instructions
To run the script, a credentials file is needed. Update the file "credentials.txt" to ocntain the following information: 
```
[auth] 
username:test 
password:test 
tenant_name:CloudCourse 
auth_url:http://94.246.116.242:5000/v2.0 
net_id: net_id 
pkey_id:pkey_id 
```
Then run the following script:
```bash
./deploy-waspmq.sh 
```

## Dependencies
```bash
$ sudo apt-get update 
$ sudo apt install python-dev python-pip  
$ export LC_ALL=C 
$ sudo pip install python-novaclient==7.1.0 
$ sudo pip install python-swiftclient
```
