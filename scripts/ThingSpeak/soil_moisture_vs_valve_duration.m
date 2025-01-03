% Read Data
soilMoisture = thingSpeakRead(channel_id, 'Fields', 1, 'NumPoints', 100, 'ReadKey', 'read_key');
valve_duration = thingSpeakRead(channel_id, 'Fields', 5, 'NumPoints', 100, 'ReadKey', 'read_key');

% Scatter Plot
figure;
scatter(soilMoisture, valve_duration, 'filled');
title('Soil Moisture vs. Valve Duration');
xlabel('Soil Moisture (%)');
ylabel('Valve Duration (s)');
grid on;
