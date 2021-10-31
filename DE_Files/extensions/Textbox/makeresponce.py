import jwt
import json
import base64
import math
from datetime import datetime


EXT_SECRET='8u0LgVBJq0gPfsx86X3LGZjRmnOg2SQp7Oh5hCbfQ8g='
EXT_CLIENT_ID='m6vu4dfjwi1lsam5tqvr5z6e3nm3oe'
EXT_OWNER_ID='5p8w7r82gcdb54mbf05vuhpsjk997c'

secret = base64.b64decode(EXT_SECRET)
ownerId = EXT_OWNER_ID
clientId = EXT_CLIENT_ID
myChannelId = 721280294


bearerPrefix = 'Bearer '
serverTokenDurationSec = 30

def makeServerToken(channelId):
    
    payload = json.dumps({
    "exp": math.floor((datetime.now()-datetime(1970,1,1)).total_seconds()) + serverTokenDurationSec,
    "channel_id": channelId,
    "user_id": ownerId, # extension owner ID for the call to Twitch PubSub
    "role": 'external',
    "pubsub_perms": {
      "send": ['*'],
    },
  })


    #app.logger.info('payload:'+payload)
    return jwt.encode(json.loads(payload), secret, algorithm="HS256")



def makeResponceBroadcast(channelId,message):

    current_count = message 

    url=f'https://api.twitch.tv/extensions/message/{channelId}'

    headers = { "Client-ID": clientId,
                "Content-Type": 'application/json',
                "Authorization": bearerPrefix + makeServerToken(channelId)}  

    body = {"content_type": 'application/json',
            "message": current_count,
            "targets": ['broadcast']} 


    return headers,body


def lambda_handler(event, context):

    # TODO implement
    
    message= base64.b64decode(event["body"]).decode('UTF-8')
    print(message)


    hd,bd=makeResponceBroadcast(myChannelId,message)


    return {
        'statusCode': 200,
        'headers' : hd,
        'body': json.dumps(bd)
    }


