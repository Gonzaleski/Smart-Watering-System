import time
import adafruit_dht
import board
import os
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from smbus2 import SMBus
import requests
from joblib import load
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Scaler
scaler = StandardScaler()

# ThingSpeak Configuration
THINGSPEAK_WRITE_API_KEY = os.getenv('THINGSPEAK_WRITE_API_KEY')
THINGSPEAK_URL = f'https://api.thingspeak.com/update?api_key={THINGSPEAK_WRITE_API_KEY}'

# Load pre-trained model
MODEL_PATH = 'model.pkl'
model = load(MODEL_PATH)

# Sensor setup
dht_sensor = adafruit_dht.DHT22(board.D17)  # GPIO17 for DHT22 data

# Setup MCP3008 for Soil Moisture Sensor (using SPI)
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
SOIL_CHANNEL = 0  # MCP3008 channel where soil moisture sensor is connected

# Setup BH1750 light sensor
BH1750_ADDRESS = 0x23
BH1750_CMD = 0x10  # Continuously High Resolution Mode
i2c_bus = SMBus(1)  # I2C bus

# Relay setup
RELAY_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def read_dht22():
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity        
        return temperature, humidity
    except RuntimeError as e:        
        print("DHT22 error:", e)
        return None, None

def read_soil_moisture():
    soil_moisture = mcp.read_adc(SOIL_CHANNEL)
    soil_moisture_percentage = ((1023 - soil_moisture) / 1023) * 100
    return soil_moisture_percentage

def read_light_sensor():
    try:
        data = i2c_bus.read_i2c_block_data(BH1750_ADDRESS, BH1750_CMD, 2)
        light_level = (data[0] << 8) | data[1]
        return light_level
    except Exception as e:
        print("BH1750 error:", e)
        return None

def send_data_to_thingspeak(temperature, humidity, soil_moisture, light_level, valve_duration):
    payload = {
        'field1': soil_moisture,
        'field2': temperature,
        'field3': humidity,
        'field4': light_level,
        'field5': valve_duration
    }
    try:
        response = requests.post(THINGSPEAK_URL, params=payload)
        if response.status_code == 200:
            print("Data sent to ThingSpeak successfully.")
        else:
            print("Failed to send data to ThingSpeak. Status code:", response.status_code)
    except Exception as e:
        print("Error sending data to ThingSpeak:", e)

try:
    while True:
        # Read sensor values
        temperature, humidity = read_dht22()
        soil_moisture = read_soil_moisture()
        light_level = read_light_sensor()

        # Print values to console
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%")
        print(f"Soil Moisture: {soil_moisture:.1f}%")  # Display percentage
        if light_level is not None:
            print(f"Light Level: {light_level} lx")

        # Prepare data for prediction
        if temperature is not None and humidity is not None and light_level is not None:
            new_data = pd.DataFrame([[soil_moisture, temperature, humidity, light_level]], columns=['Soil Moisture (%)', 'Temperature (°C)', 'Humidity (%)', 'Light Level (lx)'])
            valve_duration = model.predict(scaler.fit_transform(new_data))[0]  # Predict valve duration

            # Control the relay based on valve duration
            if valve_duration > 0.1:
                GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn on the relay
                time.sleep(valve_duration)          # Keep the valve open for the calculated duration
                GPIO.output(RELAY_PIN, GPIO.LOW)   # Turn off the relay

            print(f"Predicted Valve Duration: {valve_duration:.1f} seconds")

            # Send all sensor data and valve duration to ThingSpeak
            send_data_to_thingspeak(temperature, humidity, soil_moisture, light_level, valve_duration)

        # Wait before reading again
        time.sleep(10 * 60)  # 5 minutes
except KeyboardInterrupt:
    print("Program stopped")
finally:
    dht_sensor.exit()
    i2c_bus.close()
    GPIO.cleanup()
