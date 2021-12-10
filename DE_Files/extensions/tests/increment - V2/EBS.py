#### App.py code

from flask import Flask, render_template, Response, request, redirect, url_for, jsonify, abort, make_response
from flask_cors import CORS
#import requests

#from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import jwt
import json
import base64
import os
import math
from datetime import datetime


from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})



app = Flask(__name__)
CORS(app)



EXT_SECRET='KxQBH/gqKS95eMRXpSDPrFwfPhe2cg8A9wr7qkyfmTQ='
EXT_CLIENT_ID='l1bhofmgq6nul6piw2fygia6q8q0mq'
EXT_OWNER_ID='5p8w7r82gcdb54mbf05vuhpsjk997c'

secret = base64.b64decode(EXT_SECRET)
ownerId = EXT_OWNER_ID
clientId = EXT_CLIENT_ID

app.config["JWT_SECRET_KEY"] = secret
JWT = JWTManager(app)

bearerPrefix = 'Bearer '
serverTokenDurationSec = 30


hostUrl='localhost'
hostPort=8081

with app.app_context():
    serverOptions = jsonify({"host": hostUrl,
    "port": hostPort,
    "routes": {"cors": {"origin": ['*']}}})

channelCounts = dict()

def verifyAndDecode(header):

    #app.logger.info('header:' + header)

    if (header.startswith(bearerPrefix)):

        #app.logger.info('secret:'+ secret)

        #app.logger.info(jwt.decode(token, secret, algorithms="HS256"))
        
        try:
            token=header[len(bearerPrefix):]

            
            
            data = jwt.decode(token, secret, algorithms="HS256")
            #app.logger.info(data)

            return jwt.decode(token, secret, algorithms="HS256")

        except:
            #app.logger.info('nope1')
            abort(403, description="Invalid JWT")

    else:
        #app.logger.info('nope2')
        abort(403, description="Invalid Auth Header")

        
        


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


def makeResponceBroadcast(channelId):

    current_count = channelCounts[channelId] if channelId in channelCounts else 0 

    url=f'https://api.twitch.tv/extensions/message/{channelId}'

    headers = { "Client-ID": clientId,
                "Content-Type": 'application/json',
                "Authorization": bearerPrefix + makeServerToken(channelId)}  

    body = {"content_type": 'application/json',
            "message": current_count,
            "targets": ['broadcast']} 
    
    

    #jwt_responce = json.dumps({destination,headers,body})

    jwt_responce = make_response(body,200,headers)

    #app.logger.info('broadcast headers:'+str(jwt_responce.headers))

    #app.logger.info('broadcast body:'+jwt_responce.get_data(as_text=True))

    return jwt_responce






@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(403)
def invalid_JWT(e):
    return jsonify(error=str(e)), 403

@app.route("/count")

def index():

    return render_template('panel.html')


@app.route("/count/current", methods=['GET'])
#@jwt_required()

def HandlerCurrentIncrement():

    req = request.headers

    #app.logger.info('in current')
    #app.logger.info(req["Authorization"])

    payload = verifyAndDecode(req["Authorization"])


    channelId = payload['channel_id']
    #opaque_user_id = payload['opaqueUserId']

    current_count = channelCounts[channelId] if channelId in channelCounts else 0

    responce=makeResponceBroadcast(channelId)


    url=f'https://api.twitch.tv/extensions/message/{channelId}'

    return responce

@app.route("/count/increment", methods=['POST'])
#@jwt_required()

def HandlerIncrementQuery():

    req = request.headers

    #app.logger.info('in increment')
    #app.logger.info(req["Authorization"])

    payload = verifyAndDecode(req["Authorization"])

    
    channelId = payload['channel_id']
    #opaque_user_id = payload['opaqueUserId']

    channelCounts[channelId] = channelCounts[channelId] + 1 if channelId in channelCounts else 0

    responce=makeResponceBroadcast(channelId)


    url=f'https://api.twitch.tv/extensions/message/{channelId}'

    return responce




""" @app.route("/forward/", methods=['POST'])

def move_forward():
    #Moving forward code
    
    forward_message = "Moving Forward..."
    return render_template('panel2.html', forward_message=forward_message)
 """




#ssl_context='adhoc'
#debug=True
if __name__ == '__main__':
   app.run(port=8081,debug=True)