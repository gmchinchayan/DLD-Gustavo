# AWS part of the twitch-import

Create a text file to store the commands to launch in ec2 shell

# create an IAM user for accessing S3 buckets

access your IAM service
create a user with policy AmazonS3FullAccess

in the text file copy them with this syntax
```
export access_key='XXXXXXX'
export access_secret='xxxxxxx'
```

# create an S3 bucket

Access S3 service, create a bucket with no public access.
After creation setup Event notifications in Permissions
in event types select
    Object creation : Put
in Destination select Lambda function
in Specify lambda function
    in "Enter Lambda function ARN" field copy the ARN of the lambda created to analyse log files (Guillaume) , something like arn:aws:lambda:region:XXXXXXX:function:XXXX

in the text file copy the s3 bucket's name

```
export bucket_name='XXXXXX'
```

# Give access to the bucket to a lamba from another account
The lambda is not in the same account but it is in the same region

## Create an IAM policy to grant external access
Create a policy, here I name it CLIENT_NAME-ExtRole
Give it access to the S3 bucket create in earlier step
with PutObject, GetObject, DeleteObject and ListBucket
Your config should looks like this :
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::twitch-listener-logs/*",
                "arn:aws:s3:::twitch-listener-logs"
            ]
        }
    ]
}
```

## Create an IAM Role having this policy
Create a Role with the policy created just before

# github repo : create a personnal access token 
Please follow https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

store your username and the token in your text file

```
username XXXX
token XXXXX
```

# create the ec2 that will host the python listeners scripts
A free tier ec2 ubuntu t3.micro is ok for 5 channels followed in parallel

## updates
Connect to it and start by update the system and intall python things

```
sudo apt update
sudo apt install python3
sudo apt install python3-pip -y
pip3 install boto3
```

## git step
A change happends recently in github policy. I choose to use a personnal token to use git clone
```
git clone https://github.com/Detect-le-Defect/First_test.git
```
it will prompt you for username and password
provide your github account name and the token you've create in earlier step

## finalize the environment

Extract the directory for twitch-import scripts
Remove the github clone 

```
cp -R First_test/DE_Files/twitch-import ./
rm -Rf ./First_test/
```

Add environment variables and set executable property to sh script
don't forget the twitch parameters

```
export access_key='XXXXX'
export access_secret='XXXXX'
export bucket_name='XXXXX'
export twitch_account='XXX'
export twitch_oauth='XXX'
export twitch_app='XXX'

cd ./twitch-import
chmod a+x launch.sh
```

# launch it!
Now it is ready to use

```
./launch.sh
```



   
    