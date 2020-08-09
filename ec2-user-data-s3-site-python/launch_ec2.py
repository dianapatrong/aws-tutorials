import boto3

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2', region_name='us-east-1')

user_data = '''
    #!/bin/bash
    yum update -y
    yum install -y httpd 
    amazon-linux-extras install -y php7.2
    systemctl start httpd.service
    systemctl enable httpd.service
    aws s3 cp s3://site-for-ec2-user-data/amazons3.php /var/www/html
    '''


# Create a new EC2 instance
instance = ec2.create_instances(
    ImageId='ami-02354e95b39ca8dec',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    UserData=user_data,
    KeyName='your_key_name',
    IamInstanceProfile={
        'Name': 'EC2CopyFilesFromS3'
    },
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeleteOnTermination': True,
            'DeviceIndex': 0,
            'Groups': [
                'sg-09489316ac8b4d790',  # Security Group ID for apache-web-server-sg
            ],
            'SubnetId': 'subnet-013758ca27be668f2',  # Public Subnet ID for Tutorial Public Subnet
        },
    ],
)

