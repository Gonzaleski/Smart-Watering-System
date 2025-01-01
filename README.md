# Smart Watering System with IoT and Neural Network 🌱

## Table of Contents
- [Project Overview](#project-overview)
- [Project Components](#project-components)
  - [Hardware](#hardware)
- [Predictive Model Analysis](#predictive-model-analysis)
  - [Model Evaluation Metrics](#model-evaluation-metrics)
  - [Residual Analysis](#residual-analysis)
- [References](#references)

## **Project Overview**  
The Smart Watering System with Internet of Things (IoT) and Neural Network is a sustainable solution designed to optimize water usage in plant care. Using a combination of hardware sensors, IoT platforms, and AI models, the system monitors plant conditions and intelligently predicts watering needs, ensuring they receive just the right amount of water. This project was built as part of the [Mathworks Sustainability and Renewable Energy Challenge](https://uk.mathworks.com/academia/students/competitions/student-challenge/sustainability-and-renewable-energy-challenge.html).  

## **Project Components**  

### **Hardware**  
- [**Raspberry Pi 3 Model B+**](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/): Central hub for data collection and processing.  
- **Sensors**:  
  - [Capacitive Soil Moisture Sensor (v1.2)](https://www.amazon.co.uk/dp/B0814HXWVV/ref=pe_27063361_487055811_TE_dp_2?th=1) 
  - [DHT22 Temperature and Humidity Sensor](https://thepihut.com/products/dht22-temperature-humidity-sensor-extras)
  - [BH1750 Light Sensor](https://thepihut.com/products/adafruit-bh1750-light-sensor-stemma-qt-qwiic)
- **Actuators**:
  - [Water pump](https://www.amazon.co.uk/dp/B0814HXWVV/ref=pe_27063361_487055811_TE_dp_2?th=1)
  - [2-channel 5V relay](https://thepihut.com/products/2-channel-relay-breakout-5v)
- **Camera**
  - [Raspberry Pi Camera Module 3 NoIR](https://thepihut.com/products/raspberry-pi-camera-module-3-noir)
- **Additional Equipment**:
  - [Bread Board](https://www.amazon.co.uk/dp/B0B5TCKTQH/ref=pe_27063361_487055811_TE_dp_1)
  - [Jumper Wires](https://www.amazon.co.uk/dp/B0B5TCKTQH/ref=pe_27063361_487055811_TE_dp_1)
  - [STEMMA QT / Qwiic JST SH 4-pin to Premium Male Headers Cable (150mm Long)](https://thepihut.com/products/stemma-qt-qwiic-jst-sh-4-pin-to-premium-male-headers-cable)
  - Ethernet for stable connectivity.  
  - Soil and Cress seeds for real-world testing.
 
## **Predictive Model Analysis**
The Smart Watering System leverages machine learning models to predict the optimal duration for activating the water pump based on environmental data. To ensure high accuracy and reliability, three models were evaluated:
1. Linear Regression
2. Random Forest
3. Neural Network

### **Model Evaluation Metrics**

The performance of these models was assessed using the following metrics:
- Root Mean Square Error (RMSE): Measures the average magnitude of prediction errors.
- Mean Absolute Error (MAE): Represents the average absolute difference between predicted and actual values.
- Residuals: Highlights the distribution of prediction errors.

The following figure presents the RMSE and MAE for each model:

![alt text](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/plots/MAE_RMSE.png)

The Neural Network demonstrated the best performance, achieving the lowest MAE of 0.05 and RMSE of 0.07. This indicates that the Neural Network can make highly accurate predictions with minimal average error and few significant outliers.

The Random Forest model, while not as precise as the Neural Network, performed moderately well. With an MAE of 0.10 and RMSE of 0.15, it captured some non-linear relationships in the data but introduced more error compared to the Neural Network.

Linear Regression exhibited the highest error rates, with an MAE of 0.26 and RMSE of 0.32. This suggests that it struggled to model the complex relationships inherent in the data, likely due to its linear assumptions.

A comparative visualization of the models' RMSE and MAE is shown below, reinforcing the Neural Network's superior performance:

![alt text](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/plots/MAE_RMSE_comparison.png)

### **Residual Analysis**
Residual analysis provides deeper insights into model performance by examining the differences between actual and predicted values. The next figure shows predicted vs. actual plots for each model, along with their respective residual plots.

To facilitate a direct comparison, the following figure combines the predicted vs. actual values of all three models in a single plot and includes a distribution of residuals:

![alt text](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/plots/residuals.png)

The combined predicted vs. actual plot underscores the Neural Network’s accuracy, with its predictions clustered closest to the diagonal. Random Forest follows, while Linear Regression exhibits the greatest deviation.

The residual distribution plot further highlights the differences:

- The Neural Network has the highest peak and the narrowest domain, indicating tightly clustered residuals around zero.
- Random Forest has a lower peak and a broader spread, showing moderate variability in residuals.
- Linear Regression exhibits the lowest peak and the widest domain, reflecting larger and more inconsistent residuals.

![alt text](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/plots/residual_distribution.png)

Based on the evaluation of RMSE, MAE, and residuals, the Neural Network demonstrated the highest accuracy and consistency among the three models. It successfully captured the complex relationships in the data, making it the most suitable choice for the Smart Watering System’s predictive model. This selection ensures optimal pump activation, minimizing water wastage while maintaining plant health.

## **References**
- [Quatltrics, Interpreting Residual Plots to Improve Your Regression](https://www.qualtrics.com/support/stats-iq/analyses/regression-guides/interpreting-residual-plots-improve-regression/)
