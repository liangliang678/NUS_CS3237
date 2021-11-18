import tago
from tago import Analysis
from tago import Services
from tago import Device
import time

# Token of analysis program
ANALYSIS_TOKEN = 'b454f476-6f42-467f-8af9-27d0467d6aee'
# Token of account
ACCOUNT_TOKEN = 'e2898b73-9932-4cad-9e75-23c08127ae8a'

def calorie(walking, running, ropejumping):
  return 5.33 * walking + 10 * running + 20 * ropejumping

def get_time(time):
  real_time = time.split('T')
  real_time = real_time[1].split(':')
  real_time = int(real_time[0]) + 8
  if(real_time >= 24):
    real_time -= 24
  return real_time

def my_analysis(context, scope):
  my_account = tago.Account(ACCOUNT_TOKEN)
  my_devices = my_account.devices.list()

  for i in range(len(my_devices['result'])):
    device_token = my_account.devices.tokenList(my_devices['result'][i]['id'])
    my_device = Device(device_token['result'][0]['token'])

    filter = {
      'variable': 'result',
      'qty' : 1440,
      'start_date': '1 day'
    }

    result = my_device.find(filter)

    walking = 0
    running = 0
    ropejumping = 0
    time_info = {0:[0, 0, 0], 1:[0, 0, 0], 2:[0, 0, 0], 3:[0, 0, 0],
                 4:[0, 0, 0], 5:[0, 0, 0], 6:[0, 0, 0], 7:[0, 0, 0],
                 8:[0, 0, 0], 9:[0, 0, 0], 10:[0, 0, 0], 11:[0, 0, 0],
                 12:[0, 0, 0], 13:[0, 0, 0], 14:[0, 0, 0], 15:[0, 0, 0],
                 16:[0, 0, 0], 17:[0, 0, 0], 18:[0, 0, 0], 19:[0, 0, 0],
                 20:[0, 0, 0], 21:[0, 0, 0], 22:[0, 0, 0], 23:[0, 0, 0]}

    for j in range(0, len(result['result'])):
      if(result['result'][j]['value'] == 0):
        walking += 1
        time_info[get_time(result['result'][j]['time'])][0] += 1
      elif(result['result'][j]['value'] == 1):
        running += 1
        time_info[get_time(result['result'][j]['time'])][1] += 1
      elif(result['result'][j]['value'] == 2):
        ropejumping += 1
        time_info[get_time(result['result'][j]['time'])][2] += 1

    time_report = ''
    for k in range(24):
      if(time_info[k] != [0, 0, 0]):
        first = 1
        time_report = time_report + '%2d:00:00 - %2d:00:00:' % (k, k+1)
        if(time_info[k][0] != 0):
          if(first):
            time_report = time_report + ' walked for %d minutes' % (time_info[k][0])
          else:
            time_report = time_report + ', walked for %d minutes' % (time_info[k][0])
          first = 0
        if(time_info[k][1] != 0):
          if(first):
            time_report = time_report + ' ran for %d minutes' % (time_info[k][1])
          else:
            time_report = time_report + ', ran for %d minutes' % (time_info[k][1])
          first = 0
        if(time_info[k][2] != 0):
          if(first):
            time_report = time_report + ' ropejumped for %d minutes' % (time_info[k][2])
          else:
            time_report = time_report + ', ropejumped for %d minutes' % (time_info[k][2])
          first = 0
        time_report = time_report + '\n'
    date = time.strftime("%Y-%m-%d", time.localtime())
    email = Services(ANALYSIS_TOKEN).email
    to = my_devices['result'][i]['tags'][0]['value']
    subject = 'Exercise Summary of %s' % date
    message = 'Hi! This is today\'s exercise summary.\nYou walked for %d minutes, ran for %d minutes, ropejumped for %d minutes. You have burned %.2f calories!' % (walking, running, ropejumping, calorie(walking, running, ropejumping))
    message = message + '\ndetails:\n' + time_report 
    print(email.send(to, subject, message, None, None, None, None))
    print(to)
    print(subject)
    print(message)

Analysis(ANALYSIS_TOKEN).init(my_analysis)
