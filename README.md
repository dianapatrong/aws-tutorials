# Jumpbox Architecture

## Issue
I want to connect my EC2 instance in a private subnet of a VPC to communicate securely over the internet and be able to ping google.com


## Connecting to a private subnet
Instances within the same VPC can connect to one another through their private IP address, and therefore it is possible 
to connect to an instance in a private subnet from an instance in a public subnet.

Amazon instances require SSH keys for authentication, and we will need it to connect to the private instance as we do on 
the public one, but it is not safe at all to copy the private SSH key to the instance so we will require to forward the 
authentication request to our local machine. 
1. `sudo vi /etc/ssh/ssh_config`
2. Remove the # on the following lines so it looks like this: 
```
 Host *
 ForwardAgent yes
```

## Infrastructure


