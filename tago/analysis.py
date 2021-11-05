import json
from tago import Analysis
from tago import Device

import numpy as np
import random

TOKEN = '0144d8f4-680c-42ab-a15e-73b43bfc3ae0'

def func_callback(context, scope):
  device_token = context.environment[0]['value']
  my_device = Device(device_token)

  filter_gyro_x = {
    'variable': {'gyrox'},
    'qty' : 30
  }
  result_gyro_x = my_device.find(filter_gyro_x)
  start_data = result_gyro_x['result'][29]['time']
  end_data = result_gyro_x['result'][0]['time']

  filter_gyro_y = {
    'variable': {'gyroy'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_gyro_y = my_device.find(filter_gyro_y)

  filter_gyro_z = {
    'variable': {'gyroz'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_gyro_z = my_device.find(filter_gyro_z)

  filter_compass_x = {
    'variable': {'magx'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_compass_x = my_device.find(filter_compass_x)

  filter_compass_y = {
    'variable': {'magy'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_compass_y = my_device.find(filter_compass_y)

  filter_compass_z = {
    'variable': {'magz'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_compass_z = my_device.find(filter_compass_z)

  filter_acc_x = {
    'variable': {'accelx'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_acc_x = my_device.find(filter_acc_x)

  filter_acc_y = {
    'variable': {'accely'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_acc_y = my_device.find(filter_acc_y)

  filter_acc_z = {
    'variable': {'accelz'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_acc_z = my_device.find(filter_acc_z)

  input_array = []
  
  off = random.randint(0, len(result_gyro_x['result']) - 30)

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
  
  input_array = np.array([input_array])
  context.log(input_array)
  np.save("predict.npy", input_array)

Analysis(TOKEN).init(func_callback)
