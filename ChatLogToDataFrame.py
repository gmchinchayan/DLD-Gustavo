#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
import string
from datetime import datetime
import re
from collections import OrderedDict


# In[32]:


nickname = 'gustavo_abroad'
channel = 'greekgodx' 


# In[33]:


#Function to remove punctuation
#def message_cleaning(message):
    #Test_punc_removed = [char for char in message if char not in string.punctuation]
    #Test_punc_removed_join = ''.join(Test_punc_removed)
    #return Test_punc_removed_join


# In[34]:


def message_cleaning_duplicate(message):
    messageToshow = ''
    messagetest = message.split(' ')
    messagelist = list(OrderedDict.fromkeys(message.split(' ')))
    for word in messagelist:
         messageToshow = messageToshow + ' ' + word
    return messageToshow


# In[35]:


def add_element_to_list(time_logged_to_add,channel_to_add,username_message_to_add,messageToshow_to_add,list_to_add):
    tag_owner = 0
    if(('@' + channel) in messageToshow_to_add):
                                    tag_owner = 1
    d = {
            'Date': time_logged_to_add,
            'Channel': channel_to_add,
            'Username': username_message_to_add,
            'Message': messageToshow_to_add,
            'Tag_owner':tag_owner
        }
    list_to_add.append(d)


# In[36]:


def get_chat_dataframe(file):
    data = []

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n\n')
        for line in lines:
            try:
                time_logged = line.split('—')[0].strip()
                if(time_logged != ''):
                    time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

                username_message = line.split('—')[1:]
                infoInTheSameTime = username_message[0].split('\n\n')[1:]
                if(infoInTheSameTime):
                    firstMultiInfo = 0
                    for otherChat in infoInTheSameTime:
                        if(not firstMultiInfo):
                            messageToshow = username_message[0].split('\n\n')[0].split('#')[1:]
                            if(messageToshow):
                                channel = messageToshow[0].split(':')[0]
                                messageToshow = messageToshow[0].split(str(channel) + '' + ':')[1:][0]
                                username_message = username_message[0].split(':')[1:]
                                username_message = username_message[0].split('!')[0]
                                add_element_to_list(time_logged,channel,username_message,messageToshow,data)
                                firstMultiInfo = 1
                        messageToshow = ''
                        otherChatAtSameTime = otherChat.split(':')[1:]
                        username_message = otherChatAtSameTime[0].split('!')[0]
                        channel = otherChatAtSameTime[0].split('!')[1:]
                        for othermessage in otherChatAtSameTime[1:]:
                            messageToshow = messageToshow + '' + othermessage
                        if(channel and messageToshow and (nickname not in username_message)):
                            channel = channel[0].split('#')[1:][0]
                            add_element_to_list(time_logged,channel,username_message,messageToshow,data)

                else:
                    messageToshow = username_message[0].split('#')[1:]
                    channel = messageToshow[0].split(':')[0]
                    messageToshow = messageToshow[0].split(str(channel) + '' + ':')[1:][0]
                    username_message = username_message[0].split(':')[1:]
                    username_message = username_message[0].split('!')[0]
                    add_element_to_list(time_logged,channel,username_message,messageToshow,data)
            
            except Exception:
                pass
            
    return pd.DataFrame().from_records(data)


# In[37]:


df = get_chat_dataframe('ChatLogs/chatgreekgodx091421.log')


# In[38]:


print(df.shape)


# In[39]:


df.head(15)


# In[40]:


df.to_csv('ChatLogs/chatgreekgodx091421.csv', index=False) 


# Now, we will remove the message that only have one character, because this kind of messages are not relevant

# In[11]:


#Function to remove punctuation
#messageClean = df['Message'].apply(message_cleaning)
#df['clean_message'] = messageClean
#print(df.shape)
#df.head(15)   


# In[42]:


message_clean_duplicates = df['Message'].apply(message_cleaning_duplicate)
df['clean_message_duplicates'] = message_clean_duplicates


# In[44]:


message_to_remove_list = []
for message in df['Message']:
    if(len(message) <= 1):
        message_to_remove = df[df['Message'] == message]
        for same_messages in message_to_remove.values:
            d = {
                'Channel': same_messages[1],
                'Username': same_messages[2],
                'Message': same_messages[3]
            }
            message_to_remove_list.append(d)
            if ((df['Message'] == message) & (df['Username'] == same_messages[2])).any():
                df.drop(df[(df['Message'] == message) & (df['Username'] == same_messages[2])].index, inplace=True)
        
pd_message_to_remove =pd.DataFrame().from_records(message_to_remove_list) 

print(pd_message_to_remove.shape)
pd_message_to_remove.head(15)


# We see that we remove 119 columns

# In[45]:


print(df.shape)
df.head(15)


# Now, we need to remove spam links for bots/ persons

# In[46]:


message_to_remove_list = []
for message in df['Message']:
    if(('https' in message) or  ('.com' in message)):
        message_to_remove = df[df['Message'] == message]
        for same_messages in message_to_remove.values:
            d = {
                'Channel': same_messages[1],
                'Username': same_messages[2],
                'Message': same_messages[3]
            }
            message_to_remove_list.append(d)
            if ((df['Message'] == message) & (df['Username'] == same_messages[2])).any():
                df.drop(df[(df['Message'] == message) & (df['Username'] == same_messages[2])].index, inplace=True)

pd_message_to_remove =pd.DataFrame().from_records(message_to_remove_list) 

print(pd_message_to_remove.shape)
pd_message_to_remove.head(15)


# In[47]:


print(df.shape)
df.head(15)


# Now, we need to remove rows that contain only numbers, because they will be useless

# In[48]:


message_to_remove_list = []
for message in df['Message']:
    if(message.isnumeric() or (message.replace('-', '')).isnumeric()):
        message_to_remove = df[df['Message'] == message]
        for same_messages in message_to_remove.values:
            d = {
                'Channel': same_messages[1],
                'Username': same_messages[2],
                'Message': same_messages[3]
            }
            message_to_remove_list.append(d)
            if ((df['Message'] == message) & (df['Username'] == same_messages[2])).any():
                df.drop(df[(df['Message'] == message) & (df['Username'] == same_messages[2])].index, inplace=True)

pd_message_to_remove =pd.DataFrame().from_records(message_to_remove_list) 

print(pd_message_to_remove.shape)
pd_message_to_remove.head(15)


# In[49]:


df.to_csv('ChatLogs/chatgreekgodx091421Clean.csv', index=False) 


# In[50]:


print(df.shape)
df.head(15)


# In[ ]:


GOBLIN 


# In[ ]:




