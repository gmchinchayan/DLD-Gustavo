import logging
import logging.handlers
import requests
import json
import os
import os.path
from os import path

def check_dir(dirname):
        '''
        Check if the directory dirname exist in local, if not create it
                Parameters:
                    dirname (string): local directory name to check
        
                Returns:
                        Nothing
        '''
        # Create the directory if it does not exist
        try :
                if not path.exists(dirname):                
                        os.makedirs(dirname)
        except :
                raise Exception ("Something went wrong")

def rename_lastfile(logdir, channels):
        '''
        Rename the logfile named logdir/<channel>.log in logdir/<channel>.log.YYYY-MM-DD_HH-MI-SS
        where YYYY-MM-DD_HH-MI-SS is the first register datetime in the logfile

                Parameters:
                        logdir (string): 
                                - log directory where the files are placed
                        channels (list, optional)     
                                - List of channel and text logs 
        '''
        if type(channels) == str:
            channels = [channels]
            
        # for each channel
        for channel in channels:
            # rebuild original logfile name
            filename = logdir + '/' + channel + ".log"
           
            # Retrieve datetime into logfile
            with open(filename,encoding="utf8") as f:
                # read first line only
                first_line = f.readline()
                
                # extract date and time, replace : by - in time
                fileDate=first_line[0:10]
                fileTime=first_line[11:19].replace(":","-")
                
                # build new filename
                newname=filename+'.'+fileDate+'_'+fileTime

            # rename the file filename with it's newname
            os.rename(filename, newname)


def setup_loggers(name, log_file, level=logging.INFO):
        '''
        Setup the logger params for channel name into log_file
        Choice is to fix logs to INFO level by default
        The logfile is a rotating logfile each 30 seconds the current log_file will be rename in log_file.YYYY-MM-DD_HH-MI-SS
        where YYYY-MM-DD_HH-MI-SS is the last register datetime in the logfile

                Parameters:
                        name (string): channel name
                        log_file (string): relative path and name for the logfile
                
                returns: a logging.Logger object
        '''
        # handler part
        # general format datetime without miliseconds — message
        formatter = logging.Formatter('%(asctime)s — %(message)s',"%Y-%m-%d %H:%M:%S")
        # create a TimedRotatingFileHandler with a period of 30 seconds and base log filename is log_file  
        handler = logging.handlers.TimedRotatingFileHandler(log_file, encoding='utf-8', when="S", interval=30, backupCount=60)   
        # apply the format
        handler.setFormatter(formatter)  
        # create a logger object with channel's name

        # logger part
        # instanciate a logger with channel's name
        logger = logging.getLogger(name)
        # set it to the rigth level
        logger.setLevel(level)
        # add the handler created upper to this logger 
        logger.addHandler(handler)

        return logger