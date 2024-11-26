import subprocess
import asyncio
import os

from tapo import ApiClient
from tapo.requests import Color

from dotenv import load_dotenv

load_dotenv()

username = os.getenv('MY_APP_USERNAME')
password = os.getenv('MY_APP_PASSWORD')
bulb_address = os.getenv('BULB_ADDRESS')

async def ping_ip(ip_address):
    try:
        # Execute the ping command
        result = subprocess.run(
            ["ping", "-c", "1", ip_address],  # "-c 1" sends a single ping
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print(f"Connection to {ip_address} successful.")
        else:
            print(f"Failed to connect to {ip_address}.")

            client = ApiClient(username, password)
            device = await client.l530(bulb_address)
            await device.off()

    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(ping_ip("192.168.21.37"))
