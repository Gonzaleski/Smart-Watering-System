% displaySensorReadings.m
function displaySensorReadings(temperature, humidity, lightLevelValue, soilMoisturePercentage)
    fprintf('Temperature: %.2f °C\n', temperature);
    fprintf('Humidity: %.2f %%\n', humidity);
    fprintf('Light Level: %.2f lux\n', lightLevelValue);
    fprintf('Soil Moisture: %.2f %%\n', soilMoisturePercentage);
end