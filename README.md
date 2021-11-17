# CS3237 Project

## Setup of SensorTag App

Download the latest SensorTag App from Google Play. Connect to CC2650 Sensortag.

### Cloud View

Click on ADVANCED button, the Cloud Setup is as following:
```
Cloud service: IBM Watson IoT Platform
Username: tagoio
Password: Your device token
Broker Addres: mqtt.tago.io
Broker Port: 1883
Publish Topic: data
```
Turn on Push to Cloud switch.

### Sensors
Turn off Ambient Temperature Data, Barometer Data. Click on Humidity Data, set sensor period to 1000ms. Click on Motion Data, set sensor period to 100ms. Set Connection Contril Service to Balanced.

## Setup of Tago

### Device

Connect your sensor tag with Tago via SensorTag App (refer to [this](https://docs.tago.io/en/articles/9-mqtt-with-sensor-tag)). After adding the device, a bucket with the same name will be created automatically.

Select `Payload Parser` and enable `Run your own parser`. Copy the code in payload_parser.js into the text editor and click save. Different gateway will send different MQTT message, you may need to modify the payload parser.

Copy the default token number of the device.

### Analysis

Create two analyses, choose Python for `Runtime`, choose External for `Run this script from`. Select `Environment Variables` and add varible `device_token`, the value is what you have copied from last step.

Change the `TOKEN` varible to your `Analysis token` in analysis_rnn.py and analysis_sum.py. Run analysis_rnn.py and analysis_sum.py on your machine.

Because different gateway will send different MQTT message, names of variables may be fifferent, you may need to modify the code.

You need python3 and following library.
```
pip install -U tago
```

### Action

The first action will push data to bucket. Select MQTT Topic for `Type of trigger`, select Insert to Device Bucket for `Type of action`. Select your device and Subscribe to your MQTT Topic.

The second action will call analysis program periodically. Select Schedule for `Type of trigger`, select Run Analysis for `Type of action`. Set interval to 1 minute and select your analysis program.

The third action will call summury program periodically. Select Schedule for `Type of trigger`, select Run Analysis for `Type of action`. Set Trigger to By date and set Recurrence options as your want.

## Collecting Data
