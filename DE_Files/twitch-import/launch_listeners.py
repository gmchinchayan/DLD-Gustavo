from twitch_listener import listener
from twitch_listener import utils
import os

###############################################################################
# launch_listeners.py script
# it connect to a twitch account
# and listen a set of channels we know are actives
###############################################################################

# define directory for logs
LOGDIR = 'log'

# Connect to Twitch
# retreive in environment variables the differents parameters
twitch_account = os.environ['twitch_account']
twitch_oauth = os.environ['twitch_oauth']
twitch_app = os.environ['twitch_app']

bot = listener.connect_twitch(twitch_account, 
                             twitch_oauth, 
                             twitch_app)

# check logdir is present or create it
utils.check_dir(LOGDIR)

# List of channels to connect to
channels_to_listen_to = ['SypherPK','TheGrefg','VALORANT','Chess','MontanaBlack88']

if type(channels_to_listen_to) == str:
    channels_to_listen_to = [channels_to_listen_to]

# Scrape live chat data into raw log files. (Duration is seconds)
bot.listen(LOGDIR, channels_to_listen_to, duration = 300) 

# rename the last logfiles
utils.rename_lastfile(LOGDIR, channels_to_listen_to)

