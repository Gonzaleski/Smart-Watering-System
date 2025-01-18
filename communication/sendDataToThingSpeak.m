% sendDataToThingSpeak.m
function sendDataToThingSpeak(thingspeakSender, temperature, humidity, lightLevelValue, soilMoisturePercentage)
    response = thingspeakSender.sendData(temperature, humidity, lightLevelValue, soilMoisturePercentage);
    disp('Data sent to ThingSpeak.');
end