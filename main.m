% Add folders to MATLAB path
addpath('models');
addpath('utils');
addpath('sensors');
addpath('communication');

% Clear workspace and command window
clear; clc;

% Load environment variables
envVars = readEnv('.env');
apiKey = envVars.API_KEY;

% Use the API key as needed
thingspeakSender = ThingSpeakSender(apiKey);

% Initialize system
rpi = initializeRaspberryPi();

% Check available hardware interfaces
checkSPIChannels(rpi);
checkI2CBuses(rpi);

% Initialize sensors and GPIO
mcp3008 = initializeMCP3008(rpi);
lightSensor = initializeBH1750(rpi);
relayPin = 27;
configurePin(rpi, relayPin, 'DigitalOutput');

% Load .mat model
matModelPath = 'models/neural_network_model.mat';
load(matModelPath, 'net'); % Load the trained network object

% Normalization parameters
meanValues = [56.1591, 20.1222, 59.2810, 776.4685];
stdValues = [15.3452, 8.8366, 11.2722, 444.0649];

while true
    % Read sensor data
    [temperature, humidity] = readTemperatureAndHumidity(rpi);
    lightLevelValue = readLightSensor(lightSensor);
    soilMoisturePercentage = readSoilMoisture(mcp3008);
    
    % Display sensor readings
    displaySensorReadings(temperature, humidity, lightLevelValue, soilMoisturePercentage);

    % Normalize sensor data
    inputData = [(soilMoisturePercentage - meanValues(1)) / stdValues(1), ...
                 (temperature - meanValues(2)) / stdValues(2), ...
                 (humidity - meanValues(3)) / stdValues(3), ...
                 (lightLevelValue - meanValues(4)) / stdValues(4)];

    % Predict valve duration using .mat model
    valveDuration = predict(net, inputData);

    % Control the valve
    writeDigitalPin(rpi, relayPin, 1); % Turn on valve
    pause(valveDuration); % Keep valve on for predicted duration
    writeDigitalPin(rpi, relayPin, 0); % Turn off valve

    % Display predictions
    fprintf('Valve duration: %.2f seconds\n', valveDuration);

    % Send data to ThingSpeak
    sendDataToThingSpeak(thingspeakSender, temperature, humidity, lightLevelValue, soilMoisturePercentage);

    % Delay for 2 hours
    pause(2 * 60 * 60);
end
