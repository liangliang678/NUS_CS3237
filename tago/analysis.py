import json
from tago import Analysis
from tago import Device

TOKEN = '74b9b103-637b-4ff2-80ff-94c326640122'

def func_callback(context, scope):
  device_token = context.environment[0]['value']
  my_device = Device(device_token)

  filter_gyro_x = {
    'variable': {'gyro_x'},
    'qty' : 30
  }
  result_gyro_x = my_device.find(filter_gyro_x)
  start_data = result_gyro_x['result'][29]['time']
  end_data = result_gyro_x['result'][0]['time']

  filter_gyro_y = {
    'variable': {'gyro_y'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_gyro_y = my_device.find(filter_gyro_y)

  filter_gyro_z = {
    'variable': {'gyro_z'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_gyro_z = my_device.find(filter_gyro_z)

  filter_compass_x = {
    'variable': {'compass_x'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_compass_x = my_device.find(filter_compass_x)

  filter_compass_y = {
    'variable': {'compass_y'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_compass_y = my_device.find(filter_compass_y)

  filter_compass_z = {
    'variable': {'compass_z'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_compass_z = my_device.find(filter_compass_z)

  filter_acc_x = {
    'variable': {'acc_x'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_acc_x = my_device.find(filter_acc_x)

  filter_acc_y = {
    'variable': {'acc_y'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_acc_y = my_device.find(filter_acc_y)

  filter_acc_z = {
    'variable': {'acc_z'},
    'start_data' : start_data,
    'end_data' : end_data,
    'qty' : 30
  }
  result_acc_z = my_device.find(filter_acc_z)

  input_array = []
  for i in range(0, 30):
    input_array.append([result_gyro_x['result'][i]['value'],
                  result_gyro_y['result'][i]['value'],
                  result_gyro_z['result'][i]['value'],
                  result_compass_x['result'][i]['value'],
                  result_compass_y['result'][i]['value'],
                  result_compass_z['result'][i]['value'],
                  result_acc_x['result'][i]['value'],
                  result_acc_y['result'][i]['value'],
                  result_acc_z['result'][i]['value']])
  
  context.log(input_array)

Analysis(TOKEN).init(func_callback)
