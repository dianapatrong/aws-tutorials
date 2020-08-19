# Dumbledore Points

![Dumbledore](images/dumbledore.png)
House points are awarded to students at Hogwarts that do good deeds, correctly answer a question in class, 
or win a Quidditch Match. They can also be taken away for rule-breaking. Each student earns points for his or her House, 
and at the end of the year, the House with the most points is awarded the House Cup. 

With this tutorial we will create an Slack app where we can give points for taking time to help you out but also you can 
take them away like when they forget to submit hours on BigTime. 

## Step-by-step

## Step-1: Create a database
**AWS Console** -> **Services** -> **DynamoDB** -> **Create table**

* **Table name**: DumbledorePoints
* **Primary Key**: username


## Step-2: Create a Lambda function
**AWS Console** -> **Services** -> **Lambda** -> **Create function**

* Select **Author from scratch**
* **Function name**: DumbledorePoints
* **Runtime**: Python 3.6
* **Create function**

#### Modify IAM Role
Within the function go to **Permissions** and click on the **Role name**, this will take you to **Identity and Access Management**

* Click on **Attach policies**
    - [x] AmazonDynamoDBFullAccess
    - [x] CloudWatchFullAccess

## Step-3: Create an API Gateway 
On the lambda function, click on **Add trigger**
* Select **API Gateway**
* Select **Create an API**
* **API Type**: REST API 
* Click **Add**

# TO DO 
## Step-4: Add CloudWatch as trigger
On the lambda function, click on **Add trigger**
* Select **CloudWatch Logs**
* **Log group**: /aws/lambda/DumbledorePoints
* **Filter name**: Dumbledore Points trigger Lambda
* Click **Add**

## Step-4: Slack integration
Go to `https://api.slack.com/apps` and click on **Create new app**

* **App Name**: Dumbledore Points
* **Development Slack Workspace**: < up 2 you >
* **Create App**

After creating the app select **Slash commands** -> **Create New Command**


Under **Basic Information**, look for **Signing Secret**, go to the Lambda Function
and add that as an environment variable
** **Name**: SLACK_KEY
** **Value**: < your secret > 

https://api.slack.com/authentication/verifying-requests-from-slack