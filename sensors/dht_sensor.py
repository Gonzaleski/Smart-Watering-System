import adafruit_dht

# Class to handle DHT sensor readings
class DHTSensor:
    def __init__(self, pin):
        """
        Initialize the DHTSensor class.
        
        :param pin: The GPIO pin number where the DHT22 sensor is connected
        """
        self.sensor = adafruit_dht.DHT22(pin)  # Create a DHT22 sensor instance on the specified pin

    def read(self):
        """
        Read temperature and humidity from the DHT22 sensor.
        
        :return: A tuple containing the temperature and humidity readings, or (None, None) in case of an error
        """
        try:
            # Read temperature and humidity values from the sensor
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            # Print the readings
            print("Temperature:", temperature, "ºC")
            print("Humidity:", humidity, "%")
            return temperature, humidity  # Return the temperature and humidity values
        except RuntimeError as e:
            # Handle runtime errors (e.g., sensor read errors)
            print("DHT22 error:", e)
            return None, None  # Return None values in case of an error
