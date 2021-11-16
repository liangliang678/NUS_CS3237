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
TOKEN = '74b9b103-637b-4ff2-80ff-94c326640122'

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
  for dim in range(6):
    for i in range(23):
      flag = False
      future = [data[j][dim] for j in range(i, i+6)]
      if(dim < 3):
        flag = (max(future) - min(future)) < 20
      else:
        flag = (max(future) - min(future)) < 0.2
      if(flag):
        return False
  return True

#variables = ['gyrox', 'gyroy', 'gyroz', 'accelx', 'accely', 'accelz']
variables = ['gyro_x', 'gyro_y', 'gyro_z', 'acc_x', 'acc_y', 'acc_z']

def func_callback(context, scope):
  device_token = context.environment[0]['value']
  my_device = Device(device_token)
  
  filter_gyro_x = {
    'variable': {variables[0]},
    'qty' : TOTAL_DATA
  }
  result_gyro_x = my_device.find(filter_gyro_x)
  start_date = result_gyro_x['result'][TOTAL_DATA-1]['time']
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

  prediction = {0:0, 1:0, 2:0}
  random.seed(time.perf_counter())
  testcases = np.empty(shape=[0, 30, 6])
  iteration = 0
  failure = 0
  while(iteration < SAMPLE_NUM):
    input_array = []
    off = random.randint(0, len(result_gyro_x['result']) - 30)
    for i in range(off, off+30):
      input_array.append([float(result_gyro_x['result'][i]['value']),
                    float(result_gyro_y['result'][i]['value']),
                    float(result_gyro_z['result'][i]['value']),
                    float(result_acc_x['result'][i]['value']),
                    float(result_acc_y['result'][i]['value']),
                    float(result_acc_z['result'][i]['value'])])

    if(not isValid(input_array)):
      failure += 1
      continue
    
    input_array = np.array([input_array])
    result = MODELTEST.predictSingle(model, torch.from_numpy(input_array), BATCH_SIZE)
    prediction[result] += 1
    iteration += 1

  prediction = sorted(prediction.items(), key=lambda item:item[1], reverse=True)
  print("Exersise catagory: %s. prob: %.2f" % (index_to_sport[prediction[0][0]], prediction[0][1]/SAMPLE_NUM))

  if(prediction[0][1]/SAMPLE_NUM >= 0.50):
    insert_data = {
      'd': {
        'result': prediction[0][0]
      }
    }
    insert_result = my_device.insert(insert_data)
    print(insert_result)

if __name__ == '__main__':
  Analysis(TOKEN).init(func_callback)
