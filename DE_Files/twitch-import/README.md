# Twitch import scripts

Using the library and example twich_listener created by lloyd334 in 2019 under MIT Licence
I've modified it in the way it will suit our needs : having small logs files each 30 seconds
In the original library I've modified the logging functionality to use a time rotationg logging function to slice logs on a time base

You need to
1. create Twitch application's credentials describe in README_twitch_listener.md
2. create an IAM user you've create on your aws account with access read and write grants on S3 objects
   keep the credentials for it
3. create a personal token for your github repo (replace the github account by yours in the command)
4. create an ec2 ubuntu type, a basic one is sufficient to test

Follow the document [](file:..\AWS\twitch-import-AWS.md) for steps 2 to 4


#  usage:

```sh
    ./launch.sh
```

# Python and shell scripts description
## use of twich_listener : launch_listerners.py
 
The modified library is in subdirectory twich_listener : utils.py and listener.py
They have been adapted to our needs.
The main change is to use logging.handlers.TimedRotatingFileHandler
On a period basis the original logfile is copied with a "timestamped" name and the logs continue to flow in the original logfile. We decide to have 30 seconds periods. 
the total duration of the listening is a parameter : duration.
  
A the end of the listening time many timestamped logfiles have been created (one perchannel each 30 seconds) and original logfiles remain with the lasts logs lines. After closing the logging module I rename the original logfiles to a timestamped name 

## send logfiles to s3 bucket : push_to_s3.py
The script look at the log directory and each file, except *.log (original logfiles), are upload to an S3 bucket. The renaming of the last logfiles makes them compliant with the filter and upload the last logs.

## orchestration of the 2 python scripts : launch.sh
I use a simple shell script to launch in background mode the listener launch_listerners.py , wait 45 seconds to be sure connection to twitch and first set of timestamped logfiles are created, launch the push script push_to_s3.py in backgroud mode.





