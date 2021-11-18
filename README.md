# CS3237 Project

## Directory Structure

| Directory | Function |
| -- | -- |
| ccs | codes and images of firmware running on CC2650 SensorTag |
| data | data for training RNN model |
| data_provide | scripts for data preprocessing |
| RNN | python code for RNN model |
| tago | files related to TagoIO |

## Setup of CC2650 SensorTag

Use UniFlash to load two hex image under ccs folder to your CC2650 SensorTag.

Alternatively, you can refer to [CC26x0 SimpleLink™ Bluetooth® low energy Software Stack 2.2.x](https://www.ti.com/lit/ug/swru393e/swru393e.pdf) and use example code in examples\cc2650stk\sensortag\ccs. We only modified sensortag.c and sensortag_hum.c, which are under ccs folder.

## Setup of SensorTag App

Download the latest SensorTag App from Google Play or Apple Store. Connect to CC2650 Sensortag. GUI and configuration of SensorTag App may be different on different platform.

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
Turn off Ambient Temperature Data, Barometer Data. Click on Humidity Data, set sensor period to 1000ms. Click on Motion Data, set sensor period to 100ms. Set Connection Control Service to Balanced.

## Setup of Tago

### Analysis

Create two analyses, choose Python for `Runtime`, choose External for `Run this script from`.

Change the `ANALYSIS_TOKEN` variable to your `Analysis token`, change the `ACCOUNT_TOKEN` variable to your `Account token` in analysis_rnn.py and analysis_sum.py. Run analysis_rnn.py and analysis_sum.py on your machine.

Because different gateway will send different MQTT message, names of variables may be fifferent, you may need to modify the code.

You need python3 and following library.
```
pip install -U tago
```

### Action

The first action will push data to the bucket. Select MQTT Topic for `Type of trigger`, select Insert to Device Bucket for `Type of action`. Select your device and Subscribe to your MQTT Topic (which is `data`). Do notice that you need to create this action for every device.

The second action will call classification program periodically. Select Schedule for `Type of trigger`, select Run Analysis for `Type of action`. Set interval to 1 minute and select your classification analysis.

The third action will call summury program periodically. Select Schedule for `Type of trigger`, select Run Analysis for `Type of action`. Set Trigger to By date and set Recurrence options as your want. Select your summury analysis.

### Register a new device

Create a new device under `Custom MQTT` option. After adding the device, a bucket with the same name will be created automatically.

Select `Payload Parser` and enable `Run your own parser`. Copy the code in payload_parser.js into the text editor and click save. Different gateway will send different MQTT message, you may need to modify the payload parser.

In `Tags` column, add a row to store user's email address. The key is `email`, the value is email address.
