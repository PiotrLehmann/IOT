import paho.mqtt.client as mqtt
import json
import asyncio
import os

from tapo import ApiClient
from tapo.requests import Color
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('MY_APP_USERNAME')
password = os.getenv('MY_APP_PASSWORD')
mqtt_user = os.getenv('MQTT_USER')
mqtt_pwd = os.getenv('MQTT_PWD')

# Define MQTT broker and topic details
broker_ip = "192.168.21.37"
broker_port = 1883
light_command_topic = "home/lights/my_light/set"
light_state_topic = "home/lights/my_light/state"
brightness_command_topic = "home/lights/my_light/brightness/set"
brightness_state_topic = "home/lights/my_light/brightness/state"
rgb_command_topic = "home/lights/my_light/rgb/set"
rgb_state_topic = "home/lights/my_light/rgb/state"

# Initialize state variables
current_state = "OFF"
current_brightness = 0
current_rgb = [0, 0, 0]

def rgb_to_hue_saturation(rgb):
    """
    Convert RGB values to Hue and Saturation.

    Args:
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)

    Returns:
        tuple: (hue, saturation)
            hue (float): Hue angle in degrees (0 to 360)
            saturation (float): Saturation percentage (0 to 100)
    """

    # Normalize RGB values to the range [0, 1]
    r = rgb[0] / 255.0
    g = rgb[1] / 255.0
    b = rgb[2] / 255.0

    # Find the maximum and minimum values of RGB
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min

    # Calculate Hue
    if delta == 0:
        hue = 0
    elif c_max == r:
        hue = (60 * ((g - b) / delta) + 360) % 360
    elif c_max == g:
        hue = (60 * ((b - r) / delta) + 120) % 360
    elif c_max == b:
        hue = (60 * ((r - g) / delta) + 240) % 360

    # Calculate Saturation
    if c_max == 0:
        saturation = 0
    else:
        saturation = (delta / c_max) * 100  # Saturation as percentage

    return int(min(100, hue)), int(min(100, saturation))

async def setLight():
    tapo_username = username
    tapo_password = password
    ip_address = "10.42.0.100"

    client = ApiClient(tapo_username, tapo_password)
    global device
    device = await client.l530(ip_address)

async def turnOn():
    await device.on()

async def turnOff():
    await device.off()

async def setBrightness(bright255):
    bright = int(bright255 * 100/255)
    await device.set_brightness(bright)

async def setColor(current_rgb):
    hue, saturation = rgb_to_hue_saturation(current_rgb)
    await device.set_hue_saturation(hue, saturation)


# Define MQTT client callbacks
def on_message(client, userdata, msg):
    global current_state, current_brightness, current_rgb

    print(f"Received message on topic {msg.topic}: {msg.payload}")

    if msg.topic == light_command_topic:
        current_state = msg.payload.decode()
        if current_state == "ON":
            asyncio.run(turnOn())
        else:
            asyncio.run(turnOff())
        mqttc.publish(light_state_topic, current_state)
    
    elif msg.topic == brightness_command_topic:
        current_brightness = int(msg.payload.decode())
        asyncio.run(setBrightness(current_brightness))
        mqttc.publish(brightness_state_topic, current_brightness)
    
    elif msg.topic == rgb_command_topic:
        try:
            # Parse the RGB payload; attempt to handle unexpected formats
            payload = msg.payload.decode()
            if payload.startswith("[") and payload.endswith("]"):
                current_rgb = json.loads(payload)
            else:
                # If payload is not a JSON array, handle it as comma-separated values
                current_rgb = list(map(int, payload.split(",")))
            
            asyncio.run(setColor(current_rgb))
            mqttc.publish(rgb_state_topic, json.dumps(current_rgb))
        
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Failed to parse RGB payload: {payload}. Error: {e}")

asyncio.run(setLight())

# Initialize and connect the MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(mqtt_user, mqtt_pwd)
mqttc.on_message = on_message

# Connect and subscribe to command topics
mqttc.connect(broker_ip, broker_port, 60)
mqttc.subscribe(light_command_topic)
mqttc.subscribe(brightness_command_topic)
mqttc.subscribe(rgb_command_topic)

# Start the loop to process incoming messages
mqttc.loop_forever()
