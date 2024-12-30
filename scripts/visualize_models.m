% Script: visualize_models.m
% Load models and data
load('../models/neural_network_model.mat', 'net', 'X_test', 'Y_test'); % Load neural network model and test data
load('../models/random_forest_model.mat', 'rfModel'); % Load random forest model
load('../models/linear_regression_model.mat', 'linRegModel'); % Load linear regression model

% Predict
Y_pred_nn = predict(net, X_test); % Predictions from neural network
Y_pred_rf = predict(rfModel, X_test); % Predictions from random forest
Y_pred_lr = predict(linRegModel, X_test); % Predictions from linear regression

% Calculate Metrics
mae_nn = mean(abs(Y_test - Y_pred_nn)); % Mean Absolute Error for neural network
rmse_nn = sqrt(mean((Y_test - Y_pred_nn).^2)); % Root Mean Squared Error for neural network
mae_rf = mean(abs(Y_test - Y_pred_rf)); % Mean Absolute Error for random forest
rmse_rf = sqrt(mean((Y_test - Y_pred_rf).^2)); % Root Mean Squared Error for random forest
mae_lr = mean(abs(Y_test - Y_pred_lr)); % Mean Absolute Error for linear regression
rmse_lr = sqrt(mean((Y_test - Y_pred_lr).^2)); % Root Mean Squared Error for linear regression

% Display Results
fprintf('Model Performance Metrics:\n');
fprintf('Neural Network: MAE = %.2f, RMSE = %.2f\n', mae_nn, rmse_nn);
fprintf('Random Forest: MAE = %.2f, RMSE = %.2f\n', mae_rf, rmse_rf);
fprintf('Linear Regression: MAE = %.2f, RMSE = %.2f\n', mae_lr, rmse_lr);

% Residuals
residuals_nn = Y_test - Y_pred_nn; % Residuals for neural network
residuals_rf = Y_test - Y_pred_rf; % Residuals for random forest
residuals_lr = Y_test - Y_pred_lr; % Residuals for linear regression

% Plot Predicted vs Actual and Residuals (Dot Plots)
figure;

% Neural Network
subplot(3, 2, 1);
scatter(Y_test, Y_pred_nn, 'filled'); % Predicted vs Actual for neural network
hold on;
plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], 'k--'); % Ideal line
hold off;
xlabel('Actual');
ylabel('Predicted');
title('Neural Network: Predicted vs Actual');

subplot(3, 2, 2);
scatter(Y_test, residuals_nn, 'filled'); % Residuals for neural network
yline(0, 'k--'); % Zero residual line
xlabel('Actual');
ylabel('Residual');
title('Neural Network: Residuals');

% Random Forest
subplot(3, 2, 3);
scatter(Y_test, Y_pred_rf, 'filled', 'red'); % Predicted vs Actual for random forest
hold on;
plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], 'k--'); % Ideal line
hold off;
xlabel('Actual');
ylabel('Predicted');
title('Random Forest: Predicted vs Actual');

subplot(3, 2, 4);
scatter(Y_test, residuals_rf, 'filled', 'red'); % Residuals for random forest
yline(0, 'k--'); % Zero residual line
xlabel('Actual');
ylabel('Residual');
title('Random Forest: Residuals');

% Linear Regression
subplot(3, 2, 5);
scatter(Y_test, Y_pred_lr, 'filled', 'green'); % Predicted vs Actual for linear regression
hold on;
plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], 'k--'); % Ideal line
hold off;
xlabel('Actual');
ylabel('Predicted');
title('Linear Regression: Predicted vs Actual');

subplot(3, 2, 6);
scatter(Y_test, residuals_lr, 'filled', 'green'); % Residuals for linear regression
yline(0, 'k--'); % Zero residual line
xlabel('Actual');
ylabel('Residual');
title('Linear Regression: Residuals');

% Plot Predicted vs Actual for All Models
figure;
subplot(2, 1, 1); % First plot in the first row
scatter(Y_test, Y_pred_nn, 'filled'); % Neural network
hold on;
scatter(Y_test, Y_pred_rf, 'filled'); % Random forest
scatter(Y_test, Y_pred_lr, 'filled'); % Linear regression
plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], 'k--'); % Ideal line
hold off;
legend('NN', 'RF', 'LR', 'Location', 'best');
xlabel('Actual');
ylabel('Predicted');
title('Predicted vs Actual');

% Density Plot of Residuals for All Models
subplot(2, 1, 2); % Second plot in the second row
[f_nn, xi_nn] = ksdensity(residuals_nn); % Density for neural network
[f_rf, xi_rf] = ksdensity(residuals_rf); % Density for random forest
[f_lr, xi_lr] = ksdensity(residuals_lr); % Density for linear regression
hold on;
plot(xi_nn, f_nn, 'LineWidth', 2, 'DisplayName', 'NN'); % Neural network
plot(xi_rf, f_rf, 'LineWidth', 2, 'DisplayName', 'RF'); % Random forest
plot(xi_lr, f_lr, 'LineWidth', 2, 'DisplayName', 'LR'); % Linear regression
yline(0, 'k--', 'DisplayName', 'Zero Residual'); % Zero residual line
hold off;
legend('NN', 'RF', 'LR', 'Location', 'best');
xlabel('Residuals');
ylabel('Density');
title('Residuals Distribution');
grid on;

% Plot MAE and RMSE for All Models
figure;
subplot(1, 2, 1);
bar([mae_nn, mae_rf, mae_lr]); % Bar plot for MAE
xticklabels({'NN', 'RF', 'LR'}); % Model labels
ylabel('MAE');
title('Mean Absolute Error');

subplot(1, 2, 2);
bar([rmse_nn, rmse_rf, rmse_lr]); % Bar plot for RMSE
xticklabels({'NN', 'RF', 'LR'}); % Model labels
ylabel('RMSE');
title('Root Mean Squared Error');

% Overall Comparison of Metrics
figure;
bar(categorical({'NN', 'RF', 'LR'}), [mae_nn rmse_nn; mae_rf rmse_rf; mae_lr rmse_lr]); % Bar plot for both metrics
legend('MAE', 'RMSE');
title('Overall Comparison of MAE and RMSE');
