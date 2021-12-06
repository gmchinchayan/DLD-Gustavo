import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta, date


def lambda_handler(event, context):


    print(event)
    
    df=pd.DataFrame.from_dict(json.loads(event["body"]))
    LastDate = df["Date"][np.int_(df.size/2 -1)]
    
    LastIndex =  np.int_(df.size/2 -1)

    df = df[LastIndex-60:LastIndex]
    df.fillna(0, inplace=True)
    df = df.iloc[:,1:2].values
    #I dont know how to continue here
    #Do I need to continue here put all the code and call the function that I create? Sorry is new for me hahah

        
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

    def __init__(self, num_classes, input_size, hidden_size, num_layers):
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
  
def get_forecast_values(last_date,data_predict,):
    
    final_date = pd.to_datetime(last_date) + timedelta(seconds=data_predict.size-1)
    df_index = pd.date_range(last_date, final_date, freq='1s')
    forecast_df = pd.DataFrame(data_predict, index=df_index, columns=['Forecast'])

    return forecast_df["Forecast"]
  
    
    