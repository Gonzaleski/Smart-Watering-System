% Script: train_models.m

% Set random seed for reproducibility
% This ensures consistent results every time the script is run.
rng(8);

% Load data
% The data is loaded from a CSV file into a table for processing.
filename = '../data/system_data.csv';
data = readtable(filename);

% Extract features and target
% Define the predictor variables (features) and the target variable.
X = data{:, {'SoilMoisture___', 'Temperature__C_', 'Humidity___', 'LightLevel_lx_'}};
Y = data{:, 'ValveDuration_s_'};

% Normalize the input data
% Scale the features so that they have zero mean and unit variance, which helps improve model performance.
X = normalize(X);

% Split data into training and testing sets
% Use a holdout partition to split 80% of the data for training and 20% for testing.
cv = cvpartition(size(data, 1), 'HoldOut', 0.2);
X_train = X(training(cv), :); % Training features
Y_train = Y(training(cv), :); % Training target
X_test = X(test(cv), :);      % Testing features
Y_test = Y(test(cv), :);      % Testing target

% Neural Network Model
% Define a feedforward neural network with the following layers:
% - Input layer for the features.
% - Two fully connected layers with ReLU activation for non-linearity.
% - Output layer for regression.
% - Regression layer to compute the loss during training.
layers = [
    featureInputLayer(size(X_train, 2)) % Input layer with feature size
    fullyConnectedLayer(64)            % Fully connected layer with 64 neurons
    reluLayer                          % ReLU activation function
    fullyConnectedLayer(32)            % Fully connected layer with 32 neurons
    reluLayer                          % ReLU activation function
    fullyConnectedLayer(1)             % Output layer with one neuron for regression
    regressionLayer                    % Regression layer for training
];

% Set training options for the neural network
% - Use the 'adam' optimizer.
% - Train for a maximum of 50 epochs with a batch size of 32.
% - Disable verbose output but show the training progress plot.
options = trainingOptions('adam', ...
    'MaxEpochs', 50, ...
    'MiniBatchSize', 32, ...
    'Plots', 'training-progress', ...
    'Verbose', false);

% Train the neural network
% Train the model on the training data using the defined layers and options.
net = trainNetwork(X_train, Y_train, layers, options);

% Save the trained neural network model
% Also save the testing data for later evaluation.
save('../models/neural_network_model.mat', 'net', 'X_test', 'Y_test');

% Random Forest Model
% Train a random forest regression model with 50 decision trees.
% The random seed is reset for reproducibility.
rng(0);
numTrees = 50; % Number of trees in the forest
rfModel = TreeBagger(numTrees, X_train, Y_train, 'Method', 'regression');

% Save the trained random forest model
% Include the testing data for later evaluation.
save('../models/random_forest_model.mat', 'rfModel', 'X_test', 'Y_test');

% Linear Regression Model
% Train a simple linear regression model on the training data.
linRegModel = fitlm(X_train, Y_train);

% Save the trained linear regression model
% Include the testing data for later evaluation.
save('../models/linear_regression_model.mat', 'linRegModel', 'X_test', 'Y_test');
