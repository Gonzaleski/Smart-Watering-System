from smbus2 import SMBus

# Class to handle the light sensor readings
class LightSensor:
    def __init__(self, address=0x23):
        """
        Initialize the LightSensor class.
        
        :param address: The I2C address of the light sensor (default is 0x23 for BH1750)
        """
        self.address = address  # Set the I2C address for the light sensor
        self.i2c_bus = SMBus(1)  # Create an SMBus instance for I2C communication on bus 1

    def read(self):
        """
        Read the light level from the light sensor.
        
        :return: The light level in lux, or None in case of an error
        """
        try:
            # Read 2 bytes of data from the light sensor
            data = self.i2c_bus.read_i2c_block_data(self.address, 0x10, 2)
            # Convert the received data to the light level
            light_level = (data[0] << 8) | data[1]
            # Print the light level
            print("Light Level:", light_level, "lux")
            return light_level  # Return the light level in lux
        except Exception as e:
            # Handle any exceptions that occur during reading
            print("BH1750 error:", e)
            return None  # Return None in case of an error
