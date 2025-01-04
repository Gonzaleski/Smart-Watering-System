import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Class to handle data sending to ThingSpeak
class ThingSpeak:
    def __init__(self):
        """
        Initialize the ThingSpeak class.
        
        Retrieves the ThingSpeak API key from environment variables and constructs the API URL
        for sending data.
        """
        self.api_key = os.getenv('THINGSPEAK_WRITE_API_KEY')  # Get the ThingSpeak write API key from environment
        # Construct the ThingSpeak update URL using the API key
        self.url = f'https://api.thingspeak.com/update?api_key={self.api_key}'

    def send_data(self, temperature, humidity, soil_moisture, light_level, valve_duration):
        """
        Send sensor data to ThingSpeak.
        
        :param temperature: Temperature reading to send
        :param humidity: Humidity reading to send
        :param soil_moisture: Soil moisture reading to send
        :param light_level: Light level reading to send
        :param valve_duration: Valve duration reading to send
        """
        # Create a payload with the sensor data
        payload = {
            'field1': soil_moisture,  # Soil moisture data mapped to field1
            'field2': temperature,      # Temperature data mapped to field2
            'field3': humidity,         # Humidity data mapped to field3
            'field4': light_level,      # Light level data mapped to field4
            'field5': valve_duration     # Valve duration data mapped to field5
        }
        try:
            # Send a POST request to the ThingSpeak API with the payload
            response = requests.post(self.url, params=payload)
            if response.status_code == 200:
                # Print success message if data is sent successfully
                print("Data sent to ThingSpeak successfully.")
            else:
                # Print error message if the request fails
                print("Failed to send data to ThingSpeak. Status code:", response.status_code)
        except Exception as e:
            # Handle any exceptions that occur during the request
            print("Error sending data to ThingSpeak:", e)
