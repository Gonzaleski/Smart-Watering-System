import adafruit_dht

class DHTSensor:
    def __init__(self, pin):
        self.sensor = adafruit_dht.DHT22(pin)

    def read(self):
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            print("Temperature:", temperature, "ºC")
            print("Humidity:", humidity, "%")
            return temperature, humidity
        except RuntimeError as e:
            print("DHT22 error:", e)
            return None, None
