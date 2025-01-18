% readLightSensor.m
function lightLevelValue = readLightSensor(lightSensor)
    write(lightSensor, 0x10); % Start measurement in high-resolution mode
    pause(0.2); % Wait for measurement to complete
    lightLevel = read(lightSensor, 2); % Read 2 bytes of data
    lightLevelValue = double(typecast(uint8(lightLevel), 'uint16')) / 1.2; % Convert to lux
end