% Script: test_nn_model.m
% Description: Load the trained neural network model, normalize sample data, and predict.

% Load the trained model
load('../models/neural_network_model.mat', 'net'); 

% Define normalization parameters
mean_values = [56.1591, 20.1222, 59.2810, 776.4685]; % Mean of each feature
std_values = [15.3452, 8.8366, 11.2722, 444.0649];   % Standard deviation of each feature

% Input data for testing
sample_data = [
    30.0, 25.5, 60.0, 500.0;   % Sample 1
    50.0, 30.2, 45.0, 800.0;   % Sample 2
    20.0, 20.1, 70.0, 300.0    % Sample 3
];

% Normalize input data
normalized_data = (sample_data - mean_values) ./ std_values;

% Predict using the MATLAB neural network model
predicted_valve_durations = predict(net, normalized_data);

% Display results
fprintf('Testing Neural Network Model:\n');
for i = 1:size(sample_data, 1)
    fprintf('Sample %d: Input: [%.2f, %.2f, %.2f, %.2f] -> Predicted Valve Duration: %.2f seconds\n', ...
        i, sample_data(i, 1), sample_data(i, 2), sample_data(i, 3), sample_data(i, 4), predicted_valve_durations(i));
end
