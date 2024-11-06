import paho.mqtt.client as mqtt
import time
import random
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
     style="{",
    datefmt="%Y-%m-%d %H:%M",
)

broker_address = "broker"
broker_port = 1883
mqtt_user = ""
mqtt_password = ""
topic = "sensors/light_intensity"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="LightSensorSimulator")

client.enable_logger()

# client.username_pw_set(mqtt_user, mqtt_password)

if client.connect(broker_address, broker_port) != 0:
    logging.error("Cannot connect to MQTT Broker")
    sys.exit(-1)

try:
    while True:
        light_intensity = round(random.uniform(0, 1000), 2)
        client.publish(topic, light_intensity)
        logging.info(f"Published: {light_intensity} lx on {topic} from sensor")
        time.sleep(10)
except KeyboardInterrupt:
    logging.info("Exiting...")
    client.disconnect()
