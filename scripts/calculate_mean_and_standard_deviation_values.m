% Script: Calculate Mean and Standard Deviation for Dataset Features

% Load the dataset
% Load data from a CSV file into a table structure.
filename = '../data/system_data.csv';
data = readtable(filename);

% Extract features
features = data{:, {'SoilMoisture___', 'Temperature__C_', 'Humidity___', 'LightLevel_lx_'}};

% Calculate the mean of each feature
% The mean is calculated across all rows for each feature (column).
mean_vals = mean(features, 1);

% Calculate the standard deviation of each feature
% The standard deviation is calculated across all rows for each feature (column).
std_vals = std(features, 0, 1); % 0 indicates normalization by N-1 (default for sample std deviation)

% Display the results
% Print the mean values for each feature to the command window.
fprintf('Mean Values for Each Feature:\n');
disp(mean_vals);

% Print the standard deviation values for each feature to the command window.
fprintf('Standard Deviation Values for Each Feature:\n');
disp(std_vals);
