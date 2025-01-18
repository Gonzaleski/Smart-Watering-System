% initializeBH1750.m
function lightSensor = initializeBH1750(rpi)
    lightSensorAddress = '0x23'; % Default address for BH1750
    lightSensor = i2cdev(rpi, rpi.AvailableI2CBuses{1}, lightSensorAddress);
    disp('BH1750 light sensor initialized.');
end