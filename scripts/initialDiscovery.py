import paho.mqtt.client as mqtt
import json
import os

from dotenv import load_dotenv

load_dotenv()

mqtt_user = os.getenv('MQTT_USER')
mqtt_pwd = os.getenv('MQTT_PWD')


# Define MQTT broker and discovery topic details
broker_ip = "192.168.21.37"
broker_port = 1883
discovery_topic = "homeassistant/light/my_light/config"

# Define discovery payload with RGB and brightness control
config_payload = {
    "name": "Living Room Light",
    "unique_id": "living_room_light_123",
    "command_topic": "home/lights/my_light/set",
    "state_topic": "home/lights/my_light/state",
    "brightness_command_topic": "home/lights/my_light/brightness/set",
    "brightness_state_topic": "home/lights/my_light/brightness/state",
    "rgb_command_topic": "home/lights/my_light/rgb/set",
    "rgb_state_topic": "home/lights/my_light/rgb/state",
    "brightness_scale": 255,
    "payload_on": "ON",
    "payload_off": "OFF",
    "qos": 1,
    "retain": True
}

# Initialize and connect the MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(mqtt_user, mqtt_pwd)
mqttc.connect(broker_ip, broker_port, 60)

# Publish the discovery message to create the entity in Home Assistant
mqttc.publish(discovery_topic, json.dumps(config_payload), qos=1, retain=True)

# Disconnect after publishing
mqttc.disconnect()
print("Entity discovery message sent successfully.")
