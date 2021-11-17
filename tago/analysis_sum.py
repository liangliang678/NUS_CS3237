import tago
from tago import Analysis
from tago import Services
from tago import Device
import time

# Token of analysis program
ANALYSIS_TOKEN = 'b454f476-6f42-467f-8af9-27d0467d6aee'
# Token of account
ACCOUNT_TOKEN = 'b25d1f0c-d3e5-4788-9464-a1d57c922604'

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
        runing += 1
      elif(result['result'][j]['value'] == 2):
        ropejumping += 1

    date = time.strftime("%Y-%m-%d", time.localtime())
    email = Services(ANALYSIS_TOKEN).email
    to = my_devices['result'][i]['tags'][0]['value']
    subject = 'Exercise Summary of %s' % date
    message = 'Hi! This is today\'s exercise summary.\nYou walked for %d minutes, ran for %d minutes, ropejumped for %d minutes.' % (walking, running, ropejumping)
    # print(email.send(to, subject, message, None, None, None, None))
    print(to)
    print(subject)
    print(message)

Analysis(ANALYSIS_TOKEN).init(my_analysis)
