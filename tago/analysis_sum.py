import tago
from tago import Analysis
from tago import Services
from tago import Device
import time

# Token of analysis program
ANALYSIS_TOKEN = 'b7d8bc70-54b0-444c-9658-80e28bfce188'
# Token of account
ACCOUNT_TOKEN = 'e2898b73-9932-4cad-9e75-23c08127ae8a'

def calorie(walking, running, ropejumping):
  return 5.33 * walking + 10 * running + 20 * ropejumping

def my_analysis(context, scope):
  my_account = tago.Account(ACCOUNT_TOKEN)
  my_devices = my_account.devices.list()

  for i in range(len(my_devices['result'])):
    device_token = my_account.devices.tokenList(my_devices['result'][i]['id'])
    my_device = Device(device_token['result'][0]['token'])

    filter = {
      'variable': 'result',
      'qty' : 86400,
      'start_date': '1 day'
    }

    result = my_device.find(filter)

    walking = 0
    running = 0
    ropejumping = 0
    for j in range(0, len(result['result'])):
      if(result['result'][j]['value'] == 0):
        walking += 1
      elif(result['result'][j]['value'] == 1):
        running += 1
      elif(result['result'][j]['value'] == 2):
        ropejumping += 1

    date = time.strftime("%Y-%m-%d", time.localtime())
    email = Services(ANALYSIS_TOKEN).email
    to = my_devices['result'][i]['tags'][0]['value']
    subject = 'Exercise Summary of %s' % date
    message = 'Hi! This is today\'s exercise summary.\nYou walked for %d minutes, ran for %d minutes, ropejumped for %d minutes. You have burned %.2f calories!' % (walking, running, ropejumping, calorie(walking, running, ropejumping))
    print(email.send(to, subject, message, None, None, None, None))
    print(to)
    print(subject)
    print(message)

Analysis(ANALYSIS_TOKEN).init(my_analysis)
