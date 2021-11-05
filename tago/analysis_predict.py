import json
from tago import Analysis
from tago import Device
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

import MODELTEST
import draw
import numpy as np
import random
import time

TOKEN = '0144d8f4-680c-42ab-a15e-73b43bfc3ae0'

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
# SINGLETESTPATH = 'C:\\Users\\WU\\Desktop\\NUS\\IOT\\Project\\predict(3).npy'
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


def func_callback(context, scope):
  device_token = context.environment[0]['value']
  my_device = Device(device_token)

  filter_gyro_x = {
    'variable': {'gyrox'},
    'qty' : TOTAL_DATA
  }
  result_gyro_x = my_device.find(filter_gyro_x)
  start_data = result_gyro_x['result'][TOTAL_DATA-1]['time']
  end_data = result_gyro_x['result'][0]['time']

  filter_gyro_y = {
    'variable': {'gyroy'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : TOTAL_DATA
  }
  result_gyro_y = my_device.find(filter_gyro_y)

  filter_gyro_z = {
    'variable': {'gyroz'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : TOTAL_DATA
  }
  result_gyro_z = my_device.find(filter_gyro_z)

  filter_compass_x = {
    'variable': {'magx'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : TOTAL_DATA
  }
  result_compass_x = my_device.find(filter_compass_x)

  filter_compass_y = {
    'variable': {'magy'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : TOTAL_DATA
  }
  result_compass_y = my_device.find(filter_compass_y)

  filter_compass_z = {
    'variable': {'magz'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : TOTAL_DATA
  }
  result_compass_z = my_device.find(filter_compass_z)

  filter_acc_x = {
    'variable': {'accelx'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : TOTAL_DATA
  }
  result_acc_x = my_device.find(filter_acc_x)

  filter_acc_y = {
    'variable': {'accely'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : TOTAL_DATA
  }
  result_acc_y = my_device.find(filter_acc_y)

  filter_acc_z = {
    'variable': {'accelz'},
    'start_data' : start_data,
    'end_data' : end_data,
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
    # print(off)
    for i in range(off, off+30):
      input_array.append([float(result_gyro_x['result'][i]['value']),
                    float(result_gyro_y['result'][i]['value']),
                    float(result_gyro_z['result'][i]['value']),
                    # result_compass_x['result'][i]['value'],
                    # result_compass_y['result'][i]['value'],
                    # result_compass_z['result'][i]['value'],
                    float(result_acc_x['result'][i]['value']),
                    float(result_acc_y['result'][i]['value']),
                    float(result_acc_z['result'][i]['value'])])
    # print(input_array)
    if(not isValid(input_array)):
      failure += 1
      if(failure >= 5000):
        break
      continue
    input_array = np.array([input_array])
    result = MODELTEST.predictSingle(model, torch.from_numpy(input_array), BATCH_SIZE)
    testcases = np.concatenate((testcases, input_array))
    # draw.draw(input_array, "realtime/input%d-%d.png" % (iteration, result))
    # np.save("realtime/input%d.npy" % (iteration), input_array)
    prediction[result] += 1
    iteration += 1

  prediction = sorted(prediction.items(), key=lambda item:item[1], reverse=True)
  # print(prediction)
  print("Exersise catagory: %s. prob: %.2f" % (index_to_sport[prediction[0][0]], prediction[0][1]/200))
  np.save("realtime/samples.npy", testcases)

if __name__ == '__main__':
  Analysis(TOKEN).init(func_callback)
  # print(MODELTEST.predict(model, "realtime/samples.npy", BATCH_SIZE))
