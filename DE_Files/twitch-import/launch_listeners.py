from twitch_listener import listener
from twitch_listener import utils

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

