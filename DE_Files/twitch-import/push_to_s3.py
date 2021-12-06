import os, sys
import os.path
from os import path
import boto3
from botocore.exceptions import ClientError
from time import time, sleep

# define keys for S3 bucket
access_key = 'AKIAUSHRZ5XVFRNBEMFP'
access_secret = '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'
bucket_name = 'twitch-logs'
LOGDIR = 'log'
duration = 60


def connect_to_s3():

    try:
        # Connect to S3 bucket by key
    
        s3 = boto3.client(
            's3',
            region_name="eu-west-1",
            aws_access_key_id = access_key,
            aws_secret_access_key = access_secret
        )

        return s3

    except Exception as e:
        print(e)

def push(client_s3, data_file_folder) :  
    # push all files in LOGDIR to th S3 bucket
    # and remove them from local if success

    for file in os.listdir(data_file_folder):

        try:
            print('Uploading file {0} ...'.format(file))
            
            client_s3.upload_file(
                os.path.join(data_file_folder, file),
                bucket_name,
                file
                )

            # if it is OK let's remove the local file
            print('Removing local file {0} ...'.format(file))
            os.remove(os.path.join(data_file_folder, file))

        except ClientError as e:
            print('Incorrect credential')
            print(e)

        except Exception as e:
            print(e)    


def main():
    
    client_s3 = connect_to_s3()

    # repare path , better to be in full path
    data_file_folder = os.path.join(os.getcwd(), LOGDIR)

    startTime = time()
           
    # start pushing logs
    while (time() - startTime) < duration: 
        push(client_s3, data_file_folder)
        sleep(30)


def init():
  if __name__ == '__main__':
    sys.exit(main())

init()