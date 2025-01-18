function [temperature, humidity] = readTemperatureAndHumidity(rpi)
    % generateTemperatureAndHumidity
    % Calls a Python script to read data from the DHT22 sensor.

    try
        response = system(rpi, 'python3 /home/aradskn/read_dht22.py 17');
        
        % Split the response string to get temperature and humidity
        data = strsplit(strtrim(response), ',');  % Split by comma
        temperature = str2double(data{1});         % Convert first part to double (temperature)
        humidity = str2double(data{2});            % Convert second part to double (humidity)
        
    catch e
        fprintf('Error reading DHT22 sensor: %s\n', e.message);
        % Set default values in case of failure
        temperature = NaN;
        humidity = NaN;
    end
end
