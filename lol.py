import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random

THINGSBOARD_HOST = '129.126.163.157'
ACCESS_TOKEN = 'GRitEZOlakGkUdaEpP3e'
topic = "v1/devices/me/telemetry"




client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
print("Connected") # show what is printed in terminal

#establish connection with client
client.loop_start()
print("starting") # show what is printed in terminal


def send(temp, hum):
    data=dict()
    data["temp"] = temp
    data["hum"] = hum
    data = json.dumps(data)
    client.publish(topic,data,0)

for each in range(100):
    temp = random.uniform(40, 43.5)
    hum = random.uniform(39.4, 41.2)
    send(temp, hum)
    print(temp)
    time.sleep(1)

client.loop_stop()
client.disconnect()

