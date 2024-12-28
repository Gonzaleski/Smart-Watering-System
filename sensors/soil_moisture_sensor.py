import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class SoilMoistureSensor:
    def __init__(self, spi_port=0, spi_device=0):
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spi_port, spi_device))
        self.SOIL_CHANNEL = 0

    def read(self):
        try:
            soil_moisture = self.mcp.read_adc(self.SOIL_CHANNEL)
            soil_moisture_percentage = ((1023 - soil_moisture) / 1023) * 100
            print("Soil Moisture:", soil_moisture_percentage, "%")
            return soil_moisture_percentage
        except Exception as e:
            print("Soil moisture sensor error:", e)
            return None
