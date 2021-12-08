# Twitch listener bot

An easy to use Python bot for retrieving Twitch chat data from multiple streams/channels simultaneously. Includes functionality to generate adjacency matrices between the streams, for the purpose of network modelling. All files are generated in your working directory.  

# Installation:
```
pip install twitch-listener
```


# Steps for acquiring Twitch credentials (skip if you already have these):
1) Get a twitch.tv account 
	- get one here https://www.twitch.tv/signup
2) Obtain a Twitch client id
	- Get yours by registering an app here https://dev.twitch.tv/console/apps/create
	- (You can set 'OAuth Redirect URL' to 'http://localhost')
3) Acquire a Twitch OAuth token
	- Get yours here https://twitchapps.com/tmi/

Store these values securely. You now have everything you need to use TwitchListener.

# Example usage:

```python
from twitch_listener import listener

# Connect to Twitch
bot = listener.connect_twitch('yourUsernameHere', 
                             'yourOauthHere', 
                             'yourClientIDHere')

# List of channels to connect to
channels_to_listen_to = ['Northernlion', 'DumbDog', 'DanGheesling']

# Scrape live chat data into raw log files. (Duration is seconds)
bot.listen(channels_to_listen_to, duration = 1800) 

# logs are stored in LOGDIR sub-directory
# using time rotating logs with a period of 30 seconds
# at the end don't forget to rename default log files by <LOGDIR>/<channel>.log.YYYY-MM-DD_HH-MI-SS
utils.rename_lastfile(LOGDIR, channels_to_listen_to)


