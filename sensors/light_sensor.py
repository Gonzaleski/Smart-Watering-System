from smbus2 import SMBus

class LightSensor:
    def __init__(self, address=0x23):
        self.address = address
        self.i2c_bus = SMBus(1)

    def read(self):
        try:
            data = self.i2c_bus.read_i2c_block_data(self.address, 0x10, 2)
            light_level = (data[0] << 8) | data[1]
            print("Light Level: ", light_level, " lux")
            return light_level
        except Exception as e:
            print("BH1750 error:", e)
            return None
