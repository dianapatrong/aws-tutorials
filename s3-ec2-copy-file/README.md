# Upload/download S3 files to EC2 using Python

## Step-by-step
This guide assumes that a VPC, public and private subnet have already been created, refer to the documentation: [Pre-requisites](../README.md). 

### Step-1: Create an IAM Role
We need to authorize the EC2 instance to access the bucket in S3.

**AWS Console** -> **Services** -> **IAM** -> **Roles** -> **Create role**

* Select type of trusted entity: AWS Service
* Choose a use case: EC2
* Select your use case: Allows EC2 instances to call AWS services on your behalf
* Click on **Next: Permissions**
* Attach permissions policy: select **AmazonS3FullAccess** 
* **Role name**: EC2CopyFilesFromS3
* **Role description**: Allow EC2 instances to have access to S3

![IAM Role](images/iam-role-access.png)

### Step-2: 

### Step-3: 

### Step-4: 


 Create a bucket 
 Upload the s3 file
 Launch Ec2 instance
 Copy file from s3 to ec2
 Process file and save in new file
 Upload back to s3 