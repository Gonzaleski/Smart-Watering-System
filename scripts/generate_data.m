% Define ranges for each parameter
soilMoistureRange = [30, 80];   % Soil moisture range (%)
temperatureRange = [5, 35];    % Temperature range (°C)
humidityRange = [40, 80];      % Humidity range (%)
lightLevelRange = [0, 1500];   % Light level range (lx)

% Number of samples to generate
numSamples = 500;

% Initialize arrays to hold the data
soilMoisture = zeros(numSamples, 1);
temperature = zeros(numSamples, 1);
humidity = zeros(numSamples, 1);
lightLevel = zeros(numSamples, 1);
valveDuration = zeros(numSamples, 1);

% Function to calculate valve duration
calculateValveDuration = @(soilMoisture, temperature, humidity, lightLevel) ...
    (soilMoisture <= 60) * ...     % Apply formula only if soil moisture <= 60
    max(0.0, min(3.0, ...
    5 * (1 - (soilMoisture / 60)) + ...                          % Base duration scaled by soil moisture
    max(0, (temperature - 20) * 0.05) - ...                     % Adjustment for temperature
    max(0, (humidity - 50) * 0.02) + ...                        % Adjustment for higher humidity
    (lightLevel / 2000)));                                      % Adjustment for light level

% Generate synthetic data
for i = 1:numSamples
    % Randomly generate values within specified ranges
    soilMoisture(i) = rand() * diff(soilMoistureRange) + soilMoistureRange(1);
    temperature(i) = rand() * diff(temperatureRange) + temperatureRange(1);
    humidity(i) = rand() * diff(humidityRange) + humidityRange(1);
    lightLevel(i) = rand() * diff(lightLevelRange) + lightLevelRange(1);

    % Calculate valve duration using the defined function
    valveDuration(i) = calculateValveDuration(soilMoisture(i), temperature(i), humidity(i), lightLevel(i));
end

% Create a table to store the synthetic data
dataTable = table(soilMoisture, temperature, humidity, lightLevel, valveDuration, ...
    'VariableNames', {'Soil Moisture (%)', 'Temperature (°C)', 'Humidity (%)', 'Light Level (lx)', 'Valve Duration (s)'});

% Save the table to a CSV file
writetable(dataTable, 'system_data.csv');

% Display completion message
disp('Synthetic data generation complete. Saved to "system_data.csv".');
