% readSoilMoisture.m
function soilMoisturePercentage = readSoilMoisture(mcp3008)
    soilVoltage = readVoltage(mcp3008, 0); % Read voltage from channel 0
    soilMoisturePercentage = (soilVoltage / 3.3) * 100; % Convert to percentage (assuming 3.3V max)
end