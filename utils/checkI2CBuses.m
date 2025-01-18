% checkI2CBuses.m
function checkI2CBuses(rpi)
    disp('Scanning I2C buses for devices:');
    for i = 1:length(rpi.AvailableI2CBuses)
        devices = scanI2CBus(rpi, rpi.AvailableI2CBuses{i});
        fprintf('I2C Bus %s: Found devices: %s\n', rpi.AvailableI2CBuses{i}, strjoin(devices, ', '));
    end
end