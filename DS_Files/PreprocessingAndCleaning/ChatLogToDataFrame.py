#!/usr/bin/env python
# coding: utf-8

# Import the words english dictionary to know if the word is in english and exists.

# In[2]:


import nltk
nltk.download('words')


# Import the different libraries

# In[3]:


import pandas as pd
import string
from datetime import datetime
import re
from collections import OrderedDict
import emoji


# In[4]:


from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import PorterStemmer
from spellchecker import SpellChecker
from nltk.corpus import words


# In[5]:


import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Add some variables to apply our data pre-processing/cleanning

# The document Name and folder name must be the same that we put in the scrapper when take the data notebook

# In[6]:


nickname = 'gustavo_abroad'
channel = 'riotgames' 
documentName = 'chatriotgames101821'
folderName = '/ChatLogs/chatriotgames/'


# In[7]:


new_emotes = {
    'omegalul': 2,
    'lilw': 0,
    'monkaw': -3.0,
    'waytoodank': 0,
    'ez': 2.0,
    'clap' : 3.0,
    'lul' : 2.0,
    'booba' : 1.0,
    'pepega' : -3.0,
    'feelsgoodman' : 3.0,
    'wutfac' : -3.0,
    'sadge' : -4.0,
    'kreygasm' : 3.0,
    'kappa' : 0,
    'peeposad' : -4.0,
    'pogu' : 4.0,
    'truening' : 0,
    'lulw' : 2.0,
    'feelsbadman' : -3.0,
    'pogchamp' : 3.0,
    'poggers' : 3.0,
    'heyguys' : 2.0,
    'pepehands': -2.0,
    'rip' : -2.0,
    'seemsgood' : 3.0,
    'notlikethis' : -2.0,
    'clap' : 2.0,
    'pog' : 2.0,
    'smorc' : 0,
    'dansgam' : -4.0,
    'ez' : -1.0,
    'peeposad' : -2.0,    
}


# In[8]:


twitchEmotesToUse = ["OMEGALUL", "LULW" , "monkaW", "WAYTOODANK","EZ","Clap","LUL","BOOBA", 
                     "Pepega", "FeelsGoodMan", "WutFace", "Sadge", "Kreygasm", "Kappa", "peepoSad", "PogU", "TRUENING", "monkaS"]


# In[9]:


EMOTICONS_EMO = {
    u":‑)":"Happy face or smiley",
    u":-))":"Very Happy face or smiley",
    u":-)))":"Very very Happy face or smiley",
    u":)":"Happy face or smiley",
    u":))":"Very Happy face or smiley",
    u":)))":"Very very Happy face or smiley",
    u":-]":"Happy face or smiley",
    u":]":"Happy face or smiley",
    u":-3":"Happy face smiley",
    u":3":"Happy face smiley",
    u":->":"Happy face smiley",
    u":>":"Happy face smiley",
    u"8-)":"Happy face smiley",
    u":o)":"Happy face smiley",
    u":-}":"Happy face smiley",
    u":}":"Happy face smiley",
    u":-)":"Happy face smiley",
    u":c)":"Happy face smiley",
    u":^)":"Happy face smiley",
    u"=]":"Happy face smiley",
    u"=)":"Happy face smiley",
    u":‑D":"Laughing, big grin or laugh with glasses",
    u":D":"Laughing, big grin or laugh with glasses",
    u"8‑D":"Laughing, big grin or laugh with glasses",
    u"8D":"Laughing, big grin or laugh with glasses",
    u"X‑D":"Laughing, big grin or laugh with glasses",
    u"XD":"Laughing, big grin or laugh with glasses",
    u"=D":"Laughing, big grin or laugh with glasses",
    u"=3":"Laughing, big grin or laugh with glasses",
    u"B^D":"Laughing, big grin or laugh with glasses",
    u":-))":"Very happy",
    u":-(":"Frown, sad, andry or pouting",
    u":‑(":"Frown, sad, andry or pouting",
    u":(":"Frown, sad, andry or pouting",
    u":‑c":"Frown, sad, andry or pouting",
    u":c":"Frown, sad, andry or pouting",
    u":‑<":"Frown, sad, andry or pouting",
    u":<":"Frown, sad, andry or pouting",
    u":‑[":"Frown, sad, andry or pouting",
    u":[":"Frown, sad, andry or pouting",
    u":-||":"Frown, sad, andry or pouting",
    u">:[":"Frown, sad, andry or pouting",
    u":{":"Frown, sad, andry or pouting",
    u":@":"Frown, sad, andry or pouting",
    u">:(":"Frown, sad, andry or pouting",
    u":'‑(":"Crying",
    u":'(":"Crying",
    u":'‑)":"Tears of happiness",
    u":')":"Tears of happiness",
    u"D‑':":"Horror",
    u"D:<":"Disgust",
    u"D:":"Sadness",
    u"D8":"Great dismay",
    u"D;":"Great dismay",
    u"D=":"Great dismay",
    u"DX":"Great dismay",
    u":‑O":"Surprise",
    u":O":"Surprise",
    u":‑o":"Surprise",
    u":o":"Surprise",
    u":-0":"Shock",
    u"8‑0":"Yawn",
    u">:O":"Yawn",
    u":-*":"Kiss",
    u":*":"Kiss",
    u":X":"Kiss",
    u";‑)":"Wink or smirk",
    u";)":"Wink or smirk",
    u"*-)":"Wink or smirk",
    u"*)":"Wink or smirk",
    u";‑]":"Wink or smirk",
    u";]":"Wink or smirk",
    u";^)":"Wink or smirk",
    u":‑,":"Wink or smirk",
    u";D":"Wink or smirk",
    u":‑P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"X‑P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"XP":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":‑Þ":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":Þ":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":b":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"d:":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"=p":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u">:P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":‑/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u":/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u":-[.]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u">:[(\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u">:/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u":[(\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u"=/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u"=[(\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u":L":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u"=L":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u":S":"Skeptical, annoyed, undecided, uneasy or hesitant",
    u":‑|":"Straight face",
    u":|":"Straight face",
    u":$":"Embarrassed or blushing",
    u":‑x":"Sealed lips or wearing braces or tongue-tied",
    u":x":"Sealed lips or wearing braces or tongue-tied",
    u":‑#":"Sealed lips or wearing braces or tongue-tied",
    u":#":"Sealed lips or wearing braces or tongue-tied",
    u":‑&":"Sealed lips or wearing braces or tongue-tied",
    u":&":"Sealed lips or wearing braces or tongue-tied",
    u"O:‑)":"Angel, saint or innocent",
    u"O:)":"Angel, saint or innocent",
    u"0:‑3":"Angel, saint or innocent",
    u"0:3":"Angel, saint or innocent",
    u"0:‑)":"Angel, saint or innocent",
    u"0:)":"Angel, saint or innocent",
    u":‑b":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"0;^)":"Angel, saint or innocent",
    u">:‑)":"Evil or devilish",
    u">:)":"Evil or devilish",
    u"}:‑)":"Evil or devilish",
    u"}:)":"Evil or devilish",
    u"3:‑)":"Evil or devilish",
    u"3:)":"Evil or devilish",
    u">;)":"Evil or devilish",
    u"|;‑)":"Cool",
    u"|‑O":"Bored",
    u":‑J":"Tongue-in-cheek",
    u"#‑)":"Party all night",
    u"%‑)":"Drunk or confused",
    u"%)":"Drunk or confused",
    u":-###..":"Being sick",
    u":###..":"Being sick",
    u"<:‑|":"Dump",
    u"(>_<)":"Troubled",
    u"(>_<)>":"Troubled",
    u"(';')":"Baby",
    u"(^^>``":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"(^_^;)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"(-_-;)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"(~_~;) (・.・;)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"(-_-)zzz":"Sleeping",
    u"(^_-)":"Wink",
    u"((+_+))":"Confused",
    u"(+o+)":"Confused",
    u"(o|o)":"Ultraman",
    u"^_^":"Joyful",
    u"(^_^)/":"Joyful",
    u"(^O^)／":"Joyful",
    u"(^o^)／":"Joyful",
    u"(__)":"Kowtow as a sign of respect, or dogeza for apology",
    u"_(._.)_":"Kowtow as a sign of respect, or dogeza for apology",
    u"<(_ _)>":"Kowtow as a sign of respect, or dogeza for apology",
    u"<m(__)m>":"Kowtow as a sign of respect, or dogeza for apology",
    u"m(__)m":"Kowtow as a sign of respect, or dogeza for apology",
    u"m(_ _)m":"Kowtow as a sign of respect, or dogeza for apology",
    u"('_')":"Sad or Crying",
    u"(/_;)":"Sad or Crying",
    u"(T_T) (;_;)":"Sad or Crying",
    u"(;_;":"Sad of Crying",
    u"(;_:)":"Sad or Crying",
    u"(;O;)":"Sad or Crying",
    u"(:_;)":"Sad or Crying",
    u"(ToT)":"Sad or Crying",
    u";_;":"Sad or Crying",
    u";-;":"Sad or Crying",
    u";n;":"Sad or Crying",
    u";;":"Sad or Crying",
    u"Q.Q":"Sad or Crying",
    u"T.T":"Sad or Crying",
    u"QQ":"Sad or Crying",
    u"Q_Q":"Sad or Crying",
    u"(-.-)":"Shame",
    u"(-_-)":"Shame",
    u"(一一)":"Shame",
    u"(；一_一)":"Shame",
    u"(=_=)":"Tired",
    u"(=^·^=)":"cat",
    u"(=^··^=)":"cat",
    u"=_^= ":"cat",
    u"(..)":"Looking down",
    u"(._.)":"Looking down",
    u"^m^":"Giggling with hand covering mouth",
    u"(・・?":"Confusion",
    u"(?_?)":"Confusion",
    u">^_^<":"Normal Laugh",
    u"<^!^>":"Normal Laugh",
    u"^/^":"Normal Laugh",
    u"（*^_^*）" :"Normal Laugh",
    u"(^<^) (^.^)":"Normal Laugh",
    u"(^^)":"Normal Laugh",
    u"(^.^)":"Normal Laugh",
    u"(^_^.)":"Normal Laugh",
    u"(^_^)":"Normal Laugh",
    u"(^^)":"Normal Laugh",
    u"(^J^)":"Normal Laugh",
    u"(*^.^*)":"Normal Laugh",
    u"(^—^）":"Normal Laugh",
    u"(#^.^#)":"Normal Laugh",
    u"（^—^）":"Waving",
    u"(;_;)/~~~":"Waving",
    u"(^.^)/~~~":"Waving",
    u"(-_-)/~~~ ($··)/~~~":"Waving",
    u"(T_T)/~~~":"Waving",
    u"(ToT)/~~~":"Waving",
    u"(*^0^*)":"Excited",
    u"(*_*)":"Amazed",
    u"(*_*;":"Amazed",
    u"(+_+) (@_@)":"Amazed",
    u"(*^^)v":"Laughing,Cheerful",
    u"(^_^)v":"Laughing,Cheerful",
    u"((d[-_-]b))":"Headphones,Listening to music",
    u'(-"-)':"Worried",
    u"(ーー;)":"Worried",
    u"(^0_0^)":"Eyeglasses",
    u"(＾ｖ＾)":"Happy",
    u"(＾ｕ＾)":"Happy",
    u"(^)o(^)":"Happy",
    u"(^O^)":"Happy",
    u"(^o^)":"Happy",
    u")^o^(":"Happy",
    u":O o_O":"Surprised",
    u"o_0":"Surprised",
    u"o.O":"Surpised",
    u"(o.o)":"Surprised",
    u"oO":"Surprised",
    u"(*￣m￣)":"Dissatisfied",
    u"(‘A`)":"Snubbed or Deflated"

}


# Create a function that allow us to remove duplicates words from a phrase

# In[10]:


def message_cleaning_duplicate(message):
    messageToshow = ''
    messagelist = list(OrderedDict.fromkeys(message.split(' ')))
    for word in messagelist:
         messageToshow = messageToshow + word + " "
    return messageToshow


# Create a function that tell us if we can modify or not the message (This is used it to prevent change emojis/emotes) (DRY)

# In[11]:


def cant_modify_data(text):
    return (not(text in twitchEmotesToUse) and not(text in EMOTICONS_EMO) and not(emoji.emojize(text, language='en') in  emoji.UNICODE_EMOJI['en']))


# Create a function that allow us to add a custom row in our data frame

# In[12]:


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


# Create a function that get our .txt chat and convert to data frame

# In[13]:


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


# Convert the .txt to dataFrame

# In[14]:


analyser = SentimentIntensityAnalyzer()
analyser.lexicon.update(new_emotes)


# In[15]:


df = get_chat_dataframe('..'+ folderName + documentName + '.log')


# In[16]:


print(df.shape)


# In[16]:


df.head(15)


# Save the dataframe to know how it looks before the preprocessing

# In[17]:


df.to_csv('..'+ folderName + documentName +'.csv', index=False) 


# Now we will start with the preprocessing, we will apply the next actions:  
# 1.Stemming : Stemming is the process of reducing inflected (or sometimes derived) words to their word stem, base or root form   
# 2.Removal of Stopwords  
# 3.Remove duplicate words in a phrase  
# 4.Remove words that only have one character  
# 5.Removal of Rare words  
# 6.Lemmatization : Lemmatization is similar to stemming in reducing inflected words to their word stem but differs in the way that it makes sure the root word (also called as lemma) belongs to the language.  
# 7.Spelling correction  

# We start with the lower case

# In[18]:


stemmer = PorterStemmer()
def stem_words(text):
    text_to_save = []
    for word in text.split():
        if (cant_modify_data(word)):
            text_to_save.append(stemmer.stem(word))
        else:
            text_to_save.append(word)
    return " ".join(text_to_save)


# In[19]:


df["Cleanest_message"] = df["Message"].apply(lambda text: stem_words(text))
df.head(15)


# Now we remove the stop words

# In[20]:


", ".join(stopwords.words('english'))


# In[21]:


STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

df["Cleanest_message"] = df["Cleanest_message"].apply(lambda text: remove_stopwords(text))
df.head(15)


# Now we remove the duplicate words in a phrase

# In[22]:


message_clean_duplicates = df['Cleanest_message'].apply(message_cleaning_duplicate)
df['Cleanest_message'] = message_clean_duplicates


# In[23]:


df.head(15)


# Remove words that only have one character

# In[24]:


message_to_remove_list = []
for message in df['Message']:
    words_not_duplicate = ' '.join(set(message))
    if(len(words_not_duplicate) <= 1):
        message_to_remove = df[df['Message'] == message]
        for same_messages in message_to_remove.values:
            d = {
                'Data': same_messages[0],
                'Channel': same_messages[1],
                'Username': same_messages[2],
                'Message': same_messages[3]
            }
            if d not in message_to_remove_list:
                message_to_remove_list.append(d)
            if ((df['Message'] == message) & (df['Username'] == same_messages[2])).any():
                df.drop(df[(df['Message'] == message) & (df['Username'] == same_messages[2])].index, inplace=True)
        
pd_message_to_remove =pd.DataFrame().from_records(message_to_remove_list) 

print(pd_message_to_remove.shape)
pd_message_to_remove.head(15)


# We see that we remove 305 columns

# In[25]:


print(df.shape)
df.head(15)


# We want to count the most common words

# In[26]:


cnt = Counter()
for text in df["Cleanest_message"].values:
    for word in text.split():
        cnt[word] += 1
        
mostCommon = pd.DataFrame.from_dict(cnt, orient='index',columns=['Values'] ).reset_index()
mostCommonCopy = mostCommon
mostCommonCopy.sort_values(by=['Values'],ascending=False)


# I save this list to know the most common words, maybe it will be useful later.

# In[27]:


mostCommon.to_csv('..'+ folderName + documentName + 'MostCommonWords' + '.csv', index=False) 


# We want to get the most rare words

# In[28]:


n_rare_words = 20
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-n_rare_words-1:-1]])
RAREWORDS


# Create a function to remove rare words

# In[29]:


def remove_rarewords(text):
    return " ".join([word for word in str(text).split() if word not in RAREWORDS])


# Remove the rare words

# In[30]:


df["Cleanest_message"] = df["Cleanest_message"].apply(lambda text: remove_rarewords(text))
df.head(15)


# There are several type of stemming algorithms available and one of the famous one is porter stemmer which is widely used. We can use nltk package for the same.

# Remove all the links and page spam

# In[31]:


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


# Now, we need to remove rows that contain only numbers, because they will be useless

# In[32]:


message_to_remove_list = []
for message in df['Message']:
    if(message.isnumeric() or ((message.replace('-', '')).replace('.', '')).isnumeric()):
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


# After all this preprocessing we need to verify and remove if we have or not message (maybe all the words of one message was useless)

# In[33]:


message_to_remove_list = []
for message in df['Cleanest_message']:
    if(len(message.split()) <= 1):
        if(len(message.split()) == 0):
            message_to_remove = df[df['Cleanest_message'] == message]
            for same_messages in message_to_remove.values:
                d = {
                    'Data': same_messages[0],
                    'Channel': same_messages[1],
                    'Username': same_messages[2],
                    'Message': same_messages[3]
                }
                if d not in message_to_remove_list:
                    message_to_remove_list.append(d)
                if ((df['Cleanest_message'] == message) & (df['Username'] == same_messages[2])).any():
                    df.drop(df[(df['Cleanest_message'] == message) & (df['Username'] == same_messages[2])].index, inplace=True)

        
pd_message_to_remove =pd.DataFrame().from_records(message_to_remove_list) 

print(pd_message_to_remove.shape)
pd_message_to_remove.head(15)


# Next we verify if the message that have only one words are usefull or not (if is an emote/emoji or if it exists in english at least)

# In[34]:


message_to_remove_list = []
for message in df['Cleanest_message']:
    if(len(message.split()) <= 1):
        if(not (message.split()[0] in words.words()) and cant_modify_data(message.split()[0])):
            message_to_remove = df[df['Cleanest_message'] == message]
            for same_messages in message_to_remove.values:
                d = {
                    'Data': same_messages[0],
                    'Channel': same_messages[1],
                    'Username': same_messages[2],
                    'OriginalMessage': same_messages[3],
                    'Message': same_messages[5]
                }
                if d not in message_to_remove_list:
                    message_to_remove_list.append(d)
                if ((df['Cleanest_message'] == message) & (df['Username'] == same_messages[2])).any():
                    df.drop(df[(df['Cleanest_message'] == message) & (df['Username'] == same_messages[2])].index, inplace=True)

        
pd_message_to_remove =pd.DataFrame().from_records(message_to_remove_list) 

print(pd_message_to_remove.shape)
pd_message_to_remove.head(15)


# In[35]:


print(df.shape)
df.head(15)


# We save the message that we remove to confirm if the messages removed are actually not useful

# In[46]:


pd_message_to_remove.to_csv('..'+ folderName + documentName + 'NotUsefulMessages'+ '.csv', index=False) 


# Create a function that make an spelling check for all the words. Normally, this is fast for a little data set (we will for with a data streaming), but for large data takes some times

# In[38]:


remove_words = []
def remove_unknow_words(text):
    text_to_save = []
    for word in text.split():
        if ((word in analyser.lexicon) or (not cant_modify_data(word))):
            text_to_save.append(word)
        else:
            remove_words.append(word)
    return " ".join(text_to_save)


# In[39]:


df["Cleanest_message"] = df["Cleanest_message"].apply(lambda text: remove_unknow_words(text))
pd.DataFrame(remove_words)


# With the unknow words removed we need to check if there is a empty message

# In[40]:


print(df.shape)
df.head(15)


# In[41]:


message_to_remove_list = []
for message in df['Cleanest_message']:
    if(len(message.split()) <= 1):
        if(len(message.split()) == 0):
            message_to_remove = df[df['Cleanest_message'] == message]
            for same_messages in message_to_remove.values:
                d = {
                    'Data': same_messages[0],
                    'Channel': same_messages[1],
                    'Username': same_messages[2],
                    'Message': same_messages[3]
                }
                if d not in message_to_remove_list:
                    message_to_remove_list.append(d)
                if ((df['Cleanest_message'] == message) & (df['Username'] == same_messages[2])).any():
                    df.drop(df[(df['Cleanest_message'] == message) & (df['Username'] == same_messages[2])].index, inplace=True)

        
pd_message_to_remove =pd.DataFrame().from_records(message_to_remove_list) 

print(pd_message_to_remove.shape)
pd_message_to_remove.head(15)


# In[43]:


print(df.shape)
df.head(15)


# Finally we make a speel check

# In[44]:


spell = SpellChecker()
def correct_spellings(text):
    corrected_text = []
    misspelled_words = spell.unknown(text.split())
    for word in text.split():
        if ((word in misspelled_words) and (not(word in twitchEmotesToUse)) and (not(word in EMOTICONS_EMO))):
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)


# In[45]:


df["Cleanest_message"] = df["Cleanest_message"].apply(lambda text: correct_spellings(text))
df.head(15)


# We save our cleanest data set

# In[47]:


df.to_csv('..'+ folderName + documentName + 'Clean' + '.csv', index=False) 


# In[ ]:




