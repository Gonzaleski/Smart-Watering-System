import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Class to handle the soil moisture sensor readings
class SoilMoistureSensor:
    def __init__(self, spi_port=0, spi_device=0):
        """
        Initialize the SoilMoistureSensor class.
        
        :param spi_port: The SPI port number (default is 0)
        :param spi_device: The device number (default is 0)
        """
        # Create an instance of MCP3008 with specified SPI port and device
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spi_port, spi_device))
        self.SOIL_CHANNEL = 0  # Define the channel for the soil moisture sensor

    def read(self):
        """
        Read the soil moisture level from the sensor.
        
        :return: The soil moisture percentage, or None in case of an error
        """
        try:
            # Read the analog value from the soil moisture sensor channel
            soil_moisture = self.mcp.read_adc(self.SOIL_CHANNEL)
            # Convert the analog value to a percentage (inverted scale)
            soil_moisture_percentage = ((1023 - soil_moisture) / 1023) * 100
            # Print the soil moisture percentage
            print("Soil Moisture:", soil_moisture_percentage, "%")
            return soil_moisture_percentage  # Return the soil moisture percentage
        except Exception as e:
            # Handle any exceptions that occur during reading
            print("Soil moisture sensor error:", e)
            return None  # Return None in case of an error
