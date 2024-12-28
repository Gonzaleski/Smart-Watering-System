import time
import os
from sensors.dht_sensor import DHTSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.light_sensor import LightSensor
from communication.thingspeak import ThingSpeak
from communication.dropbox import DropboxUploader
from camera.picamera_handler import PicameraHandler
import numpy as np
import onnxruntime as ort
import board
import RPi.GPIO as GPIO

# GPIO setup for the relay
RELAY_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Initialize sensors
dht_sensor = DHTSensor(pin=board.D17)  # GPIO pin for DHT22
soil_moisture_sensor = SoilMoistureSensor()
light_sensor = LightSensor()
thingspeak = ThingSpeak()
dropbox_uploader = DropboxUploader()
picamera = PicameraHandler(save_dir='/home/aradskn/Pictures')

# Load normalization parameters
mean_values = [56.1591, 20.1222, 59.2810, 776.4685]
std_values = [15.3452, 8.8366, 11.2722, 444.0649]

# Load ONNX model
onnx_model_path = "neural_net_model.onnx"
session = ort.InferenceSession(onnx_model_path)

# Get model input and output names
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

try:
    while True:
        # Read sensor values
        temperature, humidity = dht_sensor.read()
        soil_moisture = soil_moisture_sensor.read()
        light_level = light_sensor.read()

        # Predict valve duration
        if temperature is not None and humidity is not None and soil_moisture is not None and light_level is not None:
            # Prepare the input features for prediction
            features = np.array([[soil_moisture, temperature, humidity, light_level]], dtype=np.float32)
            
            # Normalize input data
            normalized_data = (features - np.array(mean_values, dtype=np.float32)) / np.array(std_values, dtype=np.float32)

            # Make prediction using the ONNX model
            predictions = session.run([output_name], {input_name: normalized_data})[0]
            valve_duration = float(predictions[0][0])
            print("Valve duration:", valve_duration, "s")

            # Activate the valve
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            time.sleep(valve_duration)
            GPIO.output(RELAY_PIN, GPIO.LOW)

            # Send data to ThingSpeak
            thingspeak.send_data(temperature, humidity, soil_moisture, light_level, valve_duration)

            # Upload image to Dropbox
            image_path = picamera.take_picture()
            if image_path:
                dropbox_uploader.upload(image_path)

        time.sleep(3 * 60 * 60)  # Delay for 3 hours
except KeyboardInterrupt:
    print("Stopping program.")
finally:
    GPIO.cleanup()
