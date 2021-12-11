import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler
import boto3

import random
import json

#see notebook for documention
        
def sliding_windows(data, seq_length):
    x = []
    y = []

    for i in range(len(data)-seq_length-1):
        _x = data[i:(i+seq_length)]
        _y = data[i+seq_length]
        x.append(_x)
        y.append(_y)

    return np.array(x),np.array(y)

class LSTM(nn.Module):

    def __init__(self, num_classes, input_size, hidden_size, num_layers,seq_length):
        super(LSTM, self).__init__()
        
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.seq_length = seq_length
        
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True)
        
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        h_0 = Variable(torch.zeros(
            self.num_layers, x.size(0), self.hidden_size))
        
        c_0 = Variable(torch.zeros(
            self.num_layers, x.size(0), self.hidden_size))
        
        # Propagate input through LSTM
        ula, (h_out, _) = self.lstm(x, (h_0, c_0))
        
        h_out = h_out.view(-1, self.hidden_size)
        
        out = self.fc(h_out)
        
        return out
    
def create_model(num_classes, input_size, hidden_size, num_layers):
    
    lstm = LSTM(num_classes, input_size, hidden_size, num_layers)

    return lstm

def get_prediction_from_model(lstm_model,x_values):
    
    lstm_model.eval()
    train_predict = lstm(x_values)

    return train_predict
  


def lambda_handler(event, context):

    #maximum of predicted point sent to extension
    NB_PREDICTIONS_SENT = 5


    print(event)
    

    seq_length = 4
    
    input_size = 1
    hidden_size = 3
    num_layers = 1

    num_classes = 1

    #load model from checkpoint (trained model)
    lstm = LSTM(num_classes, input_size, hidden_size, num_layers,seq_length)
    lstm.load_state_dict(torch.load('lstm_model'))
    lstm.eval()

    
    #processing the data
    df = pd.DataFrame(event["body"]) 
    
    sc = MinMaxScaler()
    
    data = sc.fit_transform(df)

    x,_=sliding_windows(data,seq_length)

    X = Variable(torch.Tensor(np.array(x)))
    
    #doing the prediction
    train_predict = lstm(X)
    
    data_predict = train_predict.data.numpy()
    data_predict = sc.inverse_transform(data_predict)
    
    #convert to list
    pred = np.squeeze(data_predict).tolist()
    
    #log predictions
    print(f'pred:{pred}')

    #send models results to be given the the extension
    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
	FunctionName='broadcast',
	InvocationType='Event',
	LogType='None',
	Payload=json.dumps({"body" : json.dumps({"newPoint":event["newPoint"],"predictions":pred[:NB_PREDICTIONS_SENT]}),"Channel":event["Channel"]}))

    return {'statusCode': 200}