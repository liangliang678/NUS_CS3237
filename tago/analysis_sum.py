from tago import Analysis
from tago import Services
from tago import Device
import time

TOKEN = 'b454f476-6f42-467f-8af9-27d0467d6aee'

def my_analysis(context, scope):
  device_token = context.environment[0]['value']
  my_device = Device(device_token)

  filter = {
    'variable': 'result',
    'qty' : 86400,
    'start_date': '1 day'
  }
  result = my_device.find(filter)
 
  walking = 0
  running = 0
  ropejumping = 0
  for i in range(0, len(result['result'])):
    if(result['result'][i]['value'] == 0):
      walking += 1
    elif(result['result'][i]['value'] == 1):
      runing += 1
    elif(result['result'][i]['value'] == 2):
      ropejumping += 1

  date = time.strftime("%Y-%m-%d", time.localtime())

  email = Services(TOKEN).email
  to = 'wujunliang18@mails.ucas.ac.cn'
  subject = 'Exercise Summary of %s' % date
  message = 'Hi! This is today\'s exercise summary.\nYou walked for %d minutes, ran for %d minutes, ropejumped for %d minutes.' % (walking, running, ropejumping)
  print(email.send(to, subject, message, None, None, None, None))

Analysis(TOKEN).init(my_analysis)
