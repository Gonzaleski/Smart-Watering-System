import time
import os
import datetime
import requests
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import pandas as pd
from picamera2 import Picamera2
from dotenv import load_dotenv
from joblib import load
import RPi.GPIO as GPIO
import adafruit_dht
import board
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from smbus2 import SMBus

# Load environment variables from .env file
load_dotenv()

# Load pre-trained model and scaler
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'
model = load(MODEL_PATH)
scaler = load(SCALER_PATH)

# ThingSpeak Configuration
THINGSPEAK_WRITE_API_KEY = os.getenv('THINGSPEAK_WRITE_API_KEY')
THINGSPEAK_URL = f'https://api.thingspeak.com/update?api_key={THINGSPEAK_WRITE_API_KEY}'

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

# Dropbox Configuration
APP_KEY = os.getenv("DROPBOX_APP_KEY")
REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")

# Directory to save pictures
SAVE_DIR = "/home/aradskn/Pictures"

# Picamera2 Initialization
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (3280, 2464)}))

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

def take_picture():
    """Capture an image with Picamera2."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)
    picam2.start()
    picam2.capture_file(filepath)
    picam2.stop()
    print(f"Picture saved locally as {filename}")
    return filepath

def get_dropbox_client():
    try:
        return dropbox.Dropbox(
            oauth2_refresh_token=REFRESH_TOKEN,
            app_key=APP_KEY
        )
    except dropbox.exceptions.AuthError as e:
        print(f"Authentication error: {e}")
        return None

def upload_to_dropbox(local_path):
    """Upload a file to Dropbox."""
    try:
        dropbox_client = get_dropbox_client()
        if dropbox_client is None:
            print("Could not get Dropbox client. Exiting upload.")
            return
        with open(local_path, "rb") as file:
            dropbox_path = f"/{os.path.basename(local_path)}"  # Save in the root directory
            dropbox_client.files_upload(file.read(), dropbox_path)
            print(f"Uploaded {local_path} to Dropbox at {dropbox_path}")
    except dropbox.exceptions.AuthError as e:
        print(f"Authentication error during upload: {e}")
    except Exception as e:
        print(f"Error uploading to Dropbox: {e}")

try:
    while True:
        # Read sensor values
        temperature, humidity = read_dht22()
        soil_moisture = read_soil_moisture()
        light_level = read_light_sensor()

        # Check for valid sensor data
        if temperature is None or humidity is None or light_level is None:
            print("Skipping prediction due to incomplete sensor data.")
            time.sleep(15)
            continue

        # Print values to console
        print(f"Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%")
        print(f"Soil Moisture: {soil_moisture:.1f}%")
        print(f"Light Level: {light_level} lx")

        # Prepare data for prediction
        new_data = pd.DataFrame([[soil_moisture, temperature, humidity, light_level]], 
                                columns=['Soil Moisture (%)', 'Temperature (°C)', 'Humidity (%)', 'Light Level (lx)'])
        scaled_data = scaler.transform(new_data)
        valve_duration = model.predict(scaled_data)[0]

        # Clamp the valve duration
        valve_duration = max(0.1, min(5, valve_duration))

        # Control the relay
        if valve_duration > 0.1:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn on the relay
            time.sleep(valve_duration)         # Keep the valve open for the calculated duration
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn off the relay

        print(f"Predicted Valve Duration: {valve_duration:.1f} seconds")

        # Send all sensor data and valve duration to ThingSpeak
        send_data_to_thingspeak(temperature, humidity, soil_moisture, light_level, valve_duration)

        # Capture Image and upload to Dropbox
        image_path = take_picture()
        upload_to_dropbox(image_path)

        # Wait before reading again
        time.sleep(30 * 60)    # 30 minutes
except KeyboardInterrupt:
    print("Program stopped")
finally:
    dht_sensor.exit()
    i2c_bus.close()
    GPIO.cleanup()
