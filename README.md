# Smart Watering System with IoT and Neural Network 🌱

## Table of Contents
- [Project Overview](#project-overview)
- [Project Components](#project-components)
  - [Hardware](#hardware)
- [Installation and Usage](#installation-and-usage)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Predictive Model Analysis](#predictive-model-analysis)
  - [Training Phase](#training-phase)
  - [Model Evaluation Metrics](#model-evaluation-metrics)
  - [Residual Analysis](#residual-analysis)
- [Plant Growth Time-Lapse](#plant-growth-time-lapse)
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
 
## **Installation and Usage**

### **Prerequisites**
- Hardware Components mentioned above for real-world testing
- Python 3.11
- MATLAB with Neural Network Toolbox
- ThingSpeak, Dropbox, and Dataplicity accounts

### **Steps**
1. Clone the repository:

```bash
git clone https://github.com/Gonzaleski/Smart-Watering-System.git
```

2. Go inside the reopsitory:

```bash
cd Smart-Watering-System
```

3. Install Python virtual environment package:

```bash
pip install virtualenv
```

4. Create a virtual environment:

```bash
python -m venv venv
```

5. Activate the virtual environment:

```bash
source venv/bin/activate
```

6. Install the requirements:

```bash
pip install -r requirements.txt
```

7. Create a Dropbox App:

- Login to https://www.dropbox.com/developers/apps
- Tap on `Create App`
- Select `Scoped access`
- Select `App folder`
- Give your app a name and tap on `Create App`
- In `Settings`, record your App Key
- In `Permissions`, `file.metadata.write`, `file.metadata.read`, `file.content.write`, and `file.content.read`
- Click on `Submit`

8. Get a Dropbox refresh token:

```bash
python scripts/get_refresh_token.py 
```

Record the value.

9. Create a ThingSpeak Channel:

- Login to https://thingspeak.mathworks.com/login?skipSSOCheck=true
- Tap on `New Channel`
- Give your channel a name and a description
- `Field 1: Soil Mositure (%)`
- `Field 2: Temperature (ºC)`
- `Field 3: Humidity (%)`
- `Field 4: Light (lux)`
- `Field 5: Valve Duration`
- `Save Channel`
- In `API Keys`, redord your `Write API Key`

10. Create the environmental variables:

```bash
nano .env
```

Paste the following code in it:

```bash
THINGSPEAK_WRITE_API_KEY="Your_ThingSpeak_Write_API_Key"
DROPBOX_APP_KEY="Your_Dropbox_App_Key"
DROPBOX_REFRESH_TOKEN="Refresh_Token_Recorded_Above"
```

Save the file:
- `Cntrl+X`
- `y`
- `Enter`
 
## **Predictive Model Analysis**
The Smart Watering System leverages machine learning models to predict the optimal duration for activating the water pump based on environmental data. To ensure high accuracy and reliability, three models were evaluated:
1. Linear Regression
2. Random Forest
3. Neural Network

### **Training Phase**
The script, `scripts/train_models.m`, prepares the data, trains the models, and saves them for further analysis and use. The trained models are integral to optimizing water usage by predicting the precise duration for which the valve should remain open based on environmental conditions.

By leveraging MATLAB's robust computational tools, this script simplifies the process of developing, training, and evaluating models, ensuring consistency and accuracy at every step.

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

![alt text](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/plots/residuals.png)

- Neural Network: The predicted vs. actual plot for the Neural Network aligns closely with the diagonal line, reflecting high accuracy. The residual plot shows a symmetrical distribution around zero, with no discernible patterns, indicating a well-calibrated model.
- Random Forest: While the Random Forest predicted vs. actual plot shows some deviations from the diagonal, its residuals are also symmetrically distributed with no apparent patterns, suggesting reasonable accuracy despite minor inconsistencies.
- Linear Regression: Linear Regression’s predicted vs. actual plot reveals substantial deviations, and its residual plot shows a clear pattern with a positive slope. This suggests systematic errors and a lack of flexibility in capturing complex data relationships.

To facilitate a direct comparison, the following figure combines the predicted vs. actual values of all three models in a single plot and includes a distribution of residuals:

![alt text](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/plots/residual_distribution.png)

The combined predicted vs. actual plot underscores the Neural Network’s accuracy, with its predictions clustered closest to the diagonal. Random Forest follows, while Linear Regression exhibits the greatest deviation.

The residual distribution plot further highlights the differences:

- The Neural Network has the highest peak and the narrowest domain, indicating tightly clustered residuals around zero.
- Random Forest has a lower peak and a broader spread, showing moderate variability in residuals.
- Linear Regression exhibits the lowest peak and the widest domain, reflecting larger and more inconsistent residuals.

Based on the evaluation of RMSE, MAE, and residuals, the Neural Network demonstrated the highest accuracy and consistency among the three models. It successfully captured the complex relationships in the data, making it the most suitable choice for the Smart Watering System’s predictive model. This selection ensures optimal pump activation, minimizing water wastage while maintaining plant health.

## **Plant Growth Time-Lapse**
https://github.com/user-attachments/assets/c895cc5b-4c57-4dc1-8868-7caac24ee6f7

## **References**
- [Quatltrics, Interpreting Residual Plots to Improve Your Regression](https://www.qualtrics.com/support/stats-iq/analyses/regression-guides/interpreting-residual-plots-improve-regression/)
