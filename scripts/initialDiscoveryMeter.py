import paho.mqtt.client as mqtt
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

mqtt_user = os.getenv('MQTT_USER')
mqtt_pwd = os.getenv('MQTT_PWD')

# Define MQTT broker and discovery topic details
broker_ip = "192.168.21.37"
broker_port = 1883
discovery_topic = "homeassistant/sensor/light_meter/config"
sensor_topic = "home/sensors/light_meter"
red_topic = "home/sensors/light_meter/red"
green_topic = "home/sensors/light_meter/green"
blue_topic = "home/sensors/light_meter/blue"
clear_topic = "home/sensors/light_meter/clear"

# Define discovery payload with RGB and brightness control
config_payload = {
    "name": "Light Meter",
    "unique_id": "Light Meter",
    "red_topic": red_topic,
    "green_topic": green_topic,
    "blue_topic": blue_topic,
    "clear_topic": clear_topic,
    "qos": 1,
    "retain": True
}

# Initialize and connect the MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(mqtt_user, mqtt_pwd)
mqttc.connect(broker_ip, broker_port, 60)

# Publish the discovery message to create the entity in Home Assistant
mqttc.publish(discovery_topic, json.dumps(config_payload), qos=1, retain=True)
time.sleep(1)

# Disconnect after publishing
mqttc.disconnect()
print("Entity discovery message sent successfully.")
