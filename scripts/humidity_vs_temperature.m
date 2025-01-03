% Read Data
temperature = thingSpeakRead(channel_id, 'Fields', 2, 'NumPoints', 51, 'ReadKey', 'read_key');
humidity = thingSpeakRead(channel_id, 'Fields', 3, 'NumPoints', 51, 'ReadKey', 'read_key');

% Create a grid for temperature and humidity
[T, H] = meshgrid(linspace(min(temperature), max(temperature), 100), ...
                  linspace(min(humidity), max(humidity), 100));

% Compute the density estimate
density = ksdensity([temperature, humidity], [T(:), H(:)]);

% Reshape the density matrix to match the grid
density = reshape(density, size(T));

% Create a heatmap
figure;
imagesc(linspace(min(temperature), max(temperature), 100), ...
        linspace(min(humidity), max(humidity), 100), density);
axis xy; % Correct axis orientation
colorbar; % Add a colorbar
title('Temperature vs. Humidity');
xlabel('Temperature (°C)');
ylabel('Humidity (%)');
colormap(jet); % Use a colorful colormap
