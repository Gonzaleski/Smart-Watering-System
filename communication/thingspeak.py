import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ThingSpeak:
    def __init__(self):
        self.api_key = os.getenv('THINGSPEAK_WRITE_API_KEY')
        self.url = f'https://api.thingspeak.com/update?api_key={self.api_key}'

    def send_data(self, temperature, humidity, soil_moisture, light_level, valve_duration):
        payload = {
            'field1': soil_moisture,
            'field2': temperature,
            'field3': humidity,
            'field4': light_level,
            'field5': valve_duration
        }
        try:
            response = requests.post(self.url, params=payload)
            if response.status_code == 200:
                print("Data sent to ThingSpeak successfully.")
            else:
                print("Failed to send data to ThingSpeak. Status code:", response.status_code)
        except Exception as e:
            print("Error sending data to ThingSpeak:", e)
