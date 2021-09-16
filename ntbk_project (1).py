#!/usr/bin/env python
# coding: utf-8

# In[1]:



import twitch
from twitch_chat_analyzer_mod import analyzer
import pdb


# In[2]:


clientHelix = twitch.TwitchHelix(client_id="zcmx2b7yss60bn022uizawju3drozg", client_secret="rirjohlwwvhysysc7pbj9l8acvy0lj", scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS])


# In[3]:


myOauth = clientHelix.get_oauth()
videoID = ["892647155"]


# In[4]:


userID = clientHelix.get_videos(videoID)[0].user_id
clientHelix.get_videos(videoID)


# In[5]:


Videos = clientHelix.get_videos(user_id = userID,page_size = 5)


# In[6]:


VideosIDs = []
for i in range(len(Videos)):
    VideosIDs.append(Videos[i].id)


# In[7]:


VideosChat = []


# In[8]:


for i in range(len(VideosIDs)):
    videoChat = analyzer.FromVideoId(VideosIDs[i])
    VideosChat.append(videoChat.ToDataFrame())
breakpoint()


# In[9]:


data=VideosChat[0]


# In[10]:


data


# In[13]:


df = pd.DataFrame(data, columns= ['body', 'name','is_subscriber','offset'])


# In[12]:


import pandas as pd


# In[15]:


df.head()


# In[16]:


df.to_csv (r'C:\Users\Aleksandra\Desktop\export_dataframe.csv', index = False, header=True)


# In[34]:


nltk.download()


# In[18]:


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


# In[19]:


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))


# In[20]:


sentiment_analyzer_scores("The phone is super cool.")


# In[21]:


sentiment_analyzer_scores("The phone is super COOL!")


# In[22]:


print(sentiment_analyzer_scores("Today SUX!"))


# In[23]:


sentiment_analyzer_scores("Today SUX!")


# In[24]:


sentiment_analyzer_scores("Make sure you :) or :D today!")


# In[ ]:


sentiment_analyzer_scores("Make sure you :) or :D today!"))


# In[27]:


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# In[37]:


df['scores'] = df['body'].apply(lambda Description: analyser.polarity_scores(Description))
df


# In[ ]:





# In[ ]:





# In[ ]:




