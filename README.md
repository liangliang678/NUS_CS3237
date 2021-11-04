# CS3237 Project

## Setup of Tago

### Device

Connect your sensor tag with Tago via SensorTag App (refer to [this](https://docs.tago.io/en/articles/9-mqtt-with-sensor-tag)). After adding the device, a bucket with the same name will be created automatically.

Select `Payload Parser` and enable `Run your own parser`. Copy the code in payload_parser.js into the text editor and click save. Different gateway will send different MQTT message, you may need to modify the payload parser.

Copy the default token number of the device.

### Analysis

Create a analysis, choose Python for `Runtime`, choose External for `Run this script from`. Select `Environment Variables` and add varible `device_token`, the value is what you have copied from last step.

Change the `TOKEN` varible to your `Analysis token` in analysis.py. Run analysis.py on your machine. Because different gateway will send different MQTT message, names of variables may be fifferent, you may need to modify the code.

You need python3 and following library.
```
pip install -U tago
```

### Action

The first action will push data to bucket. Select MQTT Topic for `Type of trigger`, select Insert to Device Bucket for `Type of action`. Select your device and Subscribe to your MQTT Topic.

The second action will call analysis program periodically. Select Schedule for `Type of trigger`, select Run Analysis for `Type of action`. Set interval to 1 minute and select your analysis program.

## Collecting Data
