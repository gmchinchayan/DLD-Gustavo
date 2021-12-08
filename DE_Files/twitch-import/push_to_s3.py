import os, sys
import os.path
from os import path
import boto3
from botocore.exceptions import ClientError
from time import time, sleep

###############################################################################
# push_to_s3.py script
# it connect to an S3 bucket and upload all files present in LOGDIR
# except if they are named *.log , to avoid uploading an incomplete logfile
# it remove each file uploaded
# wait 30 seconds for a new set of logfiles 
# until reaching the duration parameter (identical in the 2 scripts)
###############################################################################

# Retreive keys for S3 bucket
access_key = os.environ['access_key']
access_secret = os.environ['access_secret']
access_secret = os.environ['bucket_name']

# define log directory to look at and how long in seconds
LOGDIR = 'log'
duration = 300

def connect_to_s3():

    '''
    Function to connect to the dedicated S3 bucket
    
    Parameters : None, they are environment variables

    Returns : an client s3 object
    '''

    try:
        # Connect to S3 bucket by key
    
        s3 = boto3.client(
            's3',
            region_name="eu-north-1",
            aws_access_key_id = access_key,
            aws_secret_access_key = access_secret
        )

        return s3

    except Exception as e:
        print(e)

def push(client_s3, data_file_folder) :  
    '''
    Function to push all files in LOGDIR to the S3 bucket except *.log files 
    and remove them from local if success

    Parameters :
        client_s3 : a boto3.client object 
        data_file_folder : folder in full path to look at
    
    Returns : 
        print a comment when a file is upload or delete
    '''

    # look at data_file_folder directory
    for file in os.listdir(data_file_folder):
        
        # for each file not finishing by .log try to upload it
        if not file.endswith('log'):
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

    '''
    Main function to define in full path the logfile directory 
    open the connection to s3 blucket and loop on push function 
    on a 30 second time period (same as logfiles creation)

    Parameters : None all is in environment 

    Returns : None

    '''
    
    client_s3 = connect_to_s3()

    # Prepare path , better to be in full path
    data_file_folder = os.path.join(os.getcwd(), LOGDIR)

    startTime = time()
           
    # start pushing logs
    while (time() - startTime) < duration: 
        push(client_s3, data_file_folder)
        sleep(30)


def init():
    '''
    init Function to start main() and exit properly
    '''
  if __name__ == '__main__':
    sys.exit(main())

init()