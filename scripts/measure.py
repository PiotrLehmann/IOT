# Here will be uploaded script for printing light colour and values of its strengh from detector on raspberryPI
import board
import busio
import adafruit_apds9960.apds9960
import time
import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

load_dotenv()

mqtt_user = os.getenv('MQTT_USER')
mqtt_pwd = os.getenv('MQTT_PWD')

broker_ip = "192.168.21.37"
broker_port = 1883

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_color = True

state_topics = {
    "red": "home/sensors/light_meter/red",
    "green": "home/sensors/light_meter/green",
    "blue": "home/sensors/light_meter/blue",
    "clear": "home/sensors/light_meter/clear"
}

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(mqtt_user, mqtt_pwd)
mqttc.connect(broker_ip, broker_port, 60)
mqttc.loop_start()


try:
    while True:
        r, g, b, c = sensor.color_data
        print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r, g, b, c))
        #print(sensor.proximity())
        mqttc.publish(state_topics["red"], int(r), qos=1, retain=True)
        mqttc.publish(state_topics["green"], int(g), qos=1, retain=True)
        mqttc.publish(state_topics["blue"], int(b), qos=1, retain=True)
        mqttc.publish(state_topics["clear"], int(c), qos=1, retain=True)
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping measurements")
finally:
    mqttc.loop_stop()
    mqttc.disconnect()

