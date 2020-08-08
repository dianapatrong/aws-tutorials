# Jumpbox Architecture

A jumpbox (also called "jump servers") are often used as a best practice for accessing to a private network from an external network. 
For example, your system might include an application host that is not intended to be publicly accessible. To access it for product updates or managing system patches, you typically log in to a bastion host and then access (or “jump to”) the application host from there.

## Connecting to a private subnet
Instances within the same VPC can connect to one another through their private IP address, and therefore it is possible 
to connect to an instance in a private subnet from an instance in a public subnet, the goal for this tutorial is to ping google.com
from an instance in a private subnet. 

## Step-by-step
This guide assumes that a VPC, public and private subnet have already been created, refer to the documentation: [Pre-requisites](../README.md). 

### Step-1: NAT Gateway
Enables instances in private subnets to connect to the internet but prevent the internet from initiating a connection with those instances. 
The NAT Gateway must be deployed in the public subnet with an Elastic IP. Once it's created, a route table associated with the private subnet needs 
to point the traffic to the NAT Gateway.

**AWS Console** -> **Services** -> **VPC** -> **NAT Gateway**
* Create NAT Gateway
* Choose the **Name Tag**: my-tutorials-nat-gateway
* Choose the **subnet** (must be the public subnet we just created): Tutorial Public Subnet
* Click on **Allocate Elastic IP**
* Create NAT gateway
---
### Step-2: Route Table for private instansce
**AWS Console** -> **Services** -> **VPC** -> **Route Tables**
Go to the **Tutorial RT for Private Subnet** route table:

* Click on **Routes** tab -> **Edit routes** 
* Click on **Add route**  
* Input 0.0.0.0/0 on the **destination**  
* On the **target** select **NAT Gateway** and the NAT gateway my-tutorials-nat-gateway
* Save routes

* Go to the subnet, click on **Edit route table association** and select the **Tutorial RT for Private Subnet**
---

### Step-3: EC2 Instances
We need two instances, one in the public subnet and one in the private subnet: 

**AWS Console** -> **Services** -> **EC2**

For the public EC2 instance:
* Launch instance
* Select Amazon Linux 2 AMI 
* Select General purpose t2.micro (free tier elegible) -> Configure Instance Details
* **Network**: Tutorials_VPC
* **Subnet**: Tutorial Public Subnet
* **Auto-assign Public IP**: Enable -> Next: Add Storage -> Next: Add Tags
* Choose a **Name tag**: My First EC2 in public subnet -> Next: Configure Security Groups
* **Security Group Name**: my-sg-for-public-instance
        
    | Type      | Protocol | Port Range | Source    |
    | :---:     |   :---:  | :---:      | :---      |
    | SSH       | TCP      | 22         | 0.0.0.0/0 |
* Review and launch -> Launch (don't forget to download the key pair)

For the private EC2 instance:
* Launch instance
* Select Amazon Linux 2 AMI 
* Select General purpose t2.micro (free tier elegible) -> Configure Instance Details
* **Network**: Tutorials_VPC
* **Subnet**: Tutorial Private Subnet
* Next: Add Storage -> Next: Add Tags
* Choose a **Name tag**: My First EC2 in private subnet -> Next: Configure Security Groups
* **Security Group Name**: my-sg-for-private-instance
* Rules:

    | Type      | Protocol | Port Range | Source                    |
    | :---:     |   :---:  | :---:      | :---                      |
    | SSH       | TCP      | 22         | my-sg-for-public-instance |
    | HTTP      | TCP      | 80         | 0.0.0.0/0                 |
* Review and launch -> Launch (don't forget to download the key pair)
---

### Step-4: SSH Agent Forwarding
Amazon instances require SSH keys for authentication, and we will need it to connect to the private instance as we do on 
the public one, but it is **not safe** to copy the private SSH key to the instance so we will require to forward the 
authentication request to our local machine. 
1. `sudo vi /etc/ssh/ssh_config`
2. Remove the # on the following lines so it looks like this: 
```
 Host <public-ec2-instance-ip-address>
 ForwardAgent yes
```

> Warning: You may be tempted to use a wildcard like `Host *` to just apply this setting to all SSH connections. 
That's not really a good idea, as you'd be sharing your local SSH keys with every server you SSH into. 
They won't have direct access to the keys, but they will be able to use them as you while the connection is established. 
You should only add servers you trust and that you intend to use with agent forwarding.

---
### Step-5: ssh into the instances
* ssh into your public instance using the key `ssh -i "key_pair.pem" ec2-user@public-instance`
* ssh into the private instance within the public one  `ssh ec2-user@private-instance`
* ``ping google.com``

![Ping google.com](images/ping_google.png)


## Architecture
![Jumpbox architecture](images/JumpboxArchitecture.png)


## Clean-up

* Terminate both EC2 instances
* Delete the NAT Gateway 
* Release the Elastic IP