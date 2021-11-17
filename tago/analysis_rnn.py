import json
import numpy as np
import random
import time

import tago
from tago import Analysis
from tago import Device

import torch
import MODELTEST

# Token of analysis program
ANALYSIS_TOKEN = 'b18c2a46-bc9a-41b6-b654-c358bdbf1d0e'
# Token of account
ACCOUNT_TOKEN = 'e2898b73-9932-4cad-9e75-23c08127ae8a'

# Load the model from MODELPATH
if torch.cuda.is_available():
  device_str = 'cuda:{}'.format(0)
else:
  device_str = 'cpu'
device = torch.device(device_str)
torch.manual_seed(0)
MODELPATH = 'model.pt'
BATCH_SIZE = 10
HIDDEN_SIZE = 16
OUTPUT_SIZE = 3
checkpoint = torch.load(MODELPATH)
model = MODELTEST.RNNModel(BATCH_SIZE,HIDDEN_SIZE,OUTPUT_SIZE).to(device)
model.load_state_dict(checkpoint['model_state_dict'])

index_to_sport = {0:'walking',1:'running',2:'ropejumping'}
SAMPLE_NUM = 200
TOTAL_DATA = 400

def isValid(data):
  count = 0
  for dim in range(6):
    i = 0
    while(i < 25):
      flag = False
      future = [data[j][dim] for j in range(i, i+6)]
      if(dim < 3):
        flag = (max(future) - min(future)) < 20
      else:
        flag = (max(future) - min(future)) < 0.1
      if(flag):
        count += 1
        i += 6
        if(count == 3):
          return False
      i += 1
  return True

# iOS version
variables = ['gyrox', 'gyroy', 'gyroz', 'accelx', 'accely', 'accelz']
# Andriod version
# variables = ['gyro_x', 'gyro_y', 'gyro_z', 'acc_x', 'acc_y', 'acc_z']

def func_callback(context, scope):
  my_account = tago.Account(ACCOUNT_TOKEN)
  my_devices = my_account.devices.list()
  for i in range(len(my_devices['result'])):
    device_token = my_account.devices.tokenList(my_devices['result'][i]['id'])
    my_device = Device(device_token['result'][0]['token'])
    
    # fetch data
    filter_gyro_x = {
      'variable': {variables[0]},
      'qty' : TOTAL_DATA
    }
    result_gyro_x = my_device.find(filter_gyro_x)
    start_date = result_gyro_x['result'][len(result_gyro_x['result'])-1]['time']
    end_date = result_gyro_x['result'][0]['time']

    filter_gyro_y = {
      'variable': {variables[1]},
      'start_date' : start_date,
      'end_date' : end_date,
      'qty' : TOTAL_DATA
    }
    result_gyro_y = my_device.find(filter_gyro_y)

    filter_gyro_z = {
      'variable': {variables[2]},
      'start_date' : start_date,
      'end_date' : end_date,
      'qty' : TOTAL_DATA
    }
    result_gyro_z = my_device.find(filter_gyro_z)

    filter_acc_x = {
      'variable': {variables[3]},
      'start_date' : start_date,
      'end_date' : end_date,
      'qty' : TOTAL_DATA
    }
    result_acc_x = my_device.find(filter_acc_x)

    filter_acc_y = {
      'variable': {variables[4]},
      'start_date' : start_date,
      'end_date' : end_date,
      'qty' : TOTAL_DATA
    }
    result_acc_y = my_device.find(filter_acc_y)

    filter_acc_z = {
      'variable': {variables[5]},
      'start_date' : start_date,
      'end_date' : end_date,
      'qty' : TOTAL_DATA
    }
    result_acc_z = my_device.find(filter_acc_z)

    # do classification
    if(len(result_gyro_x['result']) >= 30):
      prediction = {0:0, 1:0, 2:0}
      random.seed(time.perf_counter())
      testcases = np.empty(shape=[0, 30, 6])
      iteration = 0
      failure = 0
      insert_flag = 1
      
      for iteration in range(SAMPLE_NUM):
        input_array = []
        off = random.randint(0, len(result_gyro_x['result']) - 30)
        for j in range(off, off+30):
          input_array.append([float(result_gyro_x['result'][j]['value']),
                              float(result_gyro_y['result'][j]['value']),
                              float(result_gyro_z['result'][j]['value']),
                              float(result_acc_x['result'][j]['value']),
                              float(result_acc_y['result'][j]['value']),
                              float(result_acc_z['result'][j]['value'])])
        # testcases = np.concatenate((testcases, np.array([input_array])))
        isvalid = isValid(input_array)
        if(not isvalid):
          failure += 1
          continue
        
        input_array = np.array([input_array])
        result = MODELTEST.predictSingle(model, torch.from_numpy(input_array), BATCH_SIZE)
        prediction[result] += 1
      
      if(failure > SAMPLE_NUM / 2):
        print("[Device %s]: Doing nothing." % (my_devices['result'][i]['name']))
        insert_flag = 0
      else:
        prediction = sorted(prediction.items(), key=lambda item:item[1], reverse=True)
        result = prediction[0][0]
        print("[Device %s] Exersise catagory: %s. prob: %.2f" % (my_devices['result'][i]['name'], index_to_sport[result], prediction[0][1]/(SAMPLE_NUM - failure)))
        if(prediction[0][1]/(SAMPLE_NUM - failure) < 0.8):
          insert_flag = 0
      
      if(insert_flag):
        # Andriod version
        '''
        insert_data = {
          'd': {
            'result': result
          }
        }
        '''
        # iOS version
        
        insert_data = {
          'result': result
        }
        
        insert_result = my_device.insert(insert_data)
        print(insert_result)

if __name__ == '__main__':
  Analysis(ANALYSIS_TOKEN).init(func_callback)
