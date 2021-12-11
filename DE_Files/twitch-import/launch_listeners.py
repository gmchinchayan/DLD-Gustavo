from twitch_listener import listener
from twitch_listener import utils
import os
import boto3
from botocore.exceptions import ClientError

# define directory for logs
LOGDIR = 'log'

# Connect to Twitch
bot = listener.connect_twitch('vomimbre', 
                             'oauth:nkfp5dv9fqbdi2uieokqfno904sqfs', 
                             'Test_App_PRO')

# check logdir is present or create it
utils.check_dir(LOGDIR)

# List of channels to connect to
channels_to_listen_to = ['Lysium','TheGrefg']

if type(channels_to_listen_to) == str:
    channels_to_listen_to = [channels_to_listen_to]

# Scrape live chat data into raw log files. (Duration is seconds)
bot.listen(LOGDIR, channels_to_listen_to, duration = 60) 

# logfiles are renamed each 30 seconds in LOGDIR/<channel>.log.YYYY-MM-DD_HH-MI-SS
# where YYYY-MM-DD_HH-MI-SS is the last register datetime in the logfile
# but not the last one, fix it renaming it in the same format name
utils.rename_lastfile(LOGDIR, channels_to_listen_to)

# define keys for S3 bucket
access_key = 'AKIAUSHRZ5XVFRNBEMFP'
access_secret = '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'
bucket_name = 'twitch-logs'

# Connect to S3 bucket by key

client_s3 = boto3.client(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = access_secret
)

# repare path , better to be in full path
data_file_folder = os.path.join(os.getcwd(), LOGDIR)

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


