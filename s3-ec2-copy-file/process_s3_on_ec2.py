from datetime import date
import boto3

session = boto3.session.Session(profile_name='dsti')

# Create bucket in S3 (it won't work if the bucket name is already taken)
s3 = session.resource('s3')
today = date.today()
bucket_name = 'video-game-sales-tutorial-' + today.strftime("%Y%m%d")
s3.create_bucket(Bucket=bucket_name)

# Upload file to bucket
s3.Bucket(bucket_name).put_object(Key='video_game_sales.csv', Body='vgsales.csv')
s3.Bucket(bucket_name).put_object(Key='get_top_sales.py', Body='get_top_sales.py')

ec2 = session.resource('ec2', region_name='us-east-1')

# Launch EC2 instance
user_data = f'''
    #!/bin/bash
    yum update -y
    yum install python3-pip -y
    aws s3 cp s3://{bucket_name}/ /home/ec2-user/ --recursive
    pip3 install pandas
    python3 get_top_sales.py
    aws s3 cp /home/ec2-user/sales_by_platform.csv s3://{bucket_name}/
    '''

instance = ec2.create_instances(
    ImageId='ami-02354e95b39ca8dec',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    UserData=user_data,
    KeyName='S20KP',
    IamInstanceProfile={
        'Name': 'EC2ReadFromS3'
    },
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeleteOnTermination': True,
            'DeviceIndex': 0,
            'Groups': [
                'sg-022cf16ade2da5ca2',  # Security Group ID for defaul (ssh)
            ],
            'SubnetId': 'subnet-013758ca27be668f2',  # Public Subnet ID for Tutorial Public Subnet
        },
    ],
)

