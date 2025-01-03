# Smart Watering System with IoT and Neural Network 🌱

## Table of Contents
- [Project Overview](#project-overview)
- [System Workflow](#system-workflow)
- [Hardware](#hardware)
- [ThingSpeak](#thingspeak)
  - [Channel Configuration](#channel-configuration)
  - [MATLAB Visualizations](#matlab-visualizations)
  - [Widgets for Real-Time Monitoring](#widgets-for-real-time-monitoring)
  - [Channel View](#channel-view)
  - [Automated Alerts and Actions](#automated-alerts-and-actions)
  - [Why ThingSpeak Matters](#why-thingspeak-matters)
  - [View the Channel Yourself!](#view-the-channel-yourself)
- [Connectivity](#connectivity)
  - [Individual Sensor Setup](#individual-sensor-setup)
  - [Complete System Wiring](#complete-system-wiring)
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

## **System Workflow**
The diagram below shows the workflow of the Smart Watering System. It demonstrates how data flows from sensors to data processing, decision-making, and ultimately, visualization and storage.

```mermaid
graph TD
    A[Start] --> B[Run main.py every 2 hours]
    B --> C[Measure sensor data using Python scripts]
    C -->|Soil Moisture| D1[soil_moisture_sensor.py]
    C -->|Temperature & Humidity| D2[dht_sensor.py]
    C -->|Light Level| D3[light_sensor.py]
    D1 --> E[Data Collected]
    D2 --> E
    D3 --> E
    E --> F[Predict Valve Duration using Neural Network model]
    F -->|Load model from neural_network_model.onnx| G[Prediction Completed]
    G --> |Water the Plant| H[Operate 5V relay to control water pump]
    H --> |Trigger Camera| I[picamera_handler.py]
    I -->|Capture Image| J[Image File]
    J -->|Save Locally| K[Local Storage on Raspberry Pi]
    J --> |Get Dropbox Access Key using the Refresh Token| P[Dropbox Access Key]
    P --> |Upload to Cloud using the Access Key| L[Dropbox Storage]
    H --> |Send Data| M[ThingSpeak Channel]
    M -->|Data Visualization and Analytics| N[ThingSpeak Dashboard]
    N -->|Send alerts such as waterlog| O[Email]
```

## **Hardware**  
- **Central hub**:
  - [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/)
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
  - Soil and Cress seeds for real-world testing
 
## **ThingSpeak**

ThingSpeak serves as the IoT cloud platform for real-time monitoring, data visualization, and analytics in the Smart Watering System. Below is an overview of how the project leverages ThingSpeak for effective data management and insights.

### **Channel Configuration**
The ThingSpeak channel is set up with the following fields:  

- **Field 1:** Soil Moisture (%)  
- **Field 2:** Temperature (ºC)  
- **Field 3:** Humidity (%)  
- **Field 4:** Light Intensity (lux)  
- **Field 5:** Valve Duration (s)  

Fields 1 to 4 log real-time sensor data, while Field 5 records predictions from the Neural Network model, which estimates the valve duration based on sensor inputs.
### **MATLAB Visualizations**
ThingSpeak integrates MATLAB for advanced data visualization and analysis. Two MATLAB scripts are used for this project:  

1. **Scatter Plot:** Visualizes the relationship between soil moisture and valve duration.  
2. **KDE Heatmap:** Displays the kernel density estimation for temperature and humidity, revealing key environmental patterns.    

### **Widgets for Real-Time Monitoring**
A **gauge widget** is configured to track soil moisture levels at a glance, with states represented as:  
- **Red:** Danger zone (below 30% or above 70%)
- **Green:** Healthy range (50% to 60%)
- **Amber:** Warning zone (anything else)

### **Channel View**
The following figures illustrate the ThingSpeak channel for this project:

![ThingSpeak Results 1](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/thingspeak/thingspeak_results_1.png) 

![ThingSpeak Results 2](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/results/thingspeak/thingspeak_results_2.png) 


#### **Key Observations:**  
- The Soil Moisture vs. Valve Duration scatter plot highlights an inverse relationship: as soil moisture increases, valve duration decreases.  
- The Temperature vs. Humidity KDE shows the plant environment is typically in the 20–21°C range with ~60% humidity.

### **Automated Alerts and Actions**
ThingSpeak's MATLAB analysis scripts and TimeControl feature automate system responses:  
- A MATLAB script runs every 6 hours to check soil moisture levels.  
- If the soil moisture enters the danger zone (below 30% or above 70%), an email notification is triggered.  

### **Why ThingSpeak Matters**
- ThingSpeak enhances the Smart Watering System by turning raw data into actionable insights and enabling proactive system management:
- Real-Time Monitoring: Visualizations of real-world data allow for consistent and reliable plant monitoring.
- Data Interpretation: MATLAB visualizations provide deeper insights, helping to analyze and understand the collected data effectively.
- Automated Responses: The integration of MATLAB Analysis and TimeControl enables automated actions, such as sending alerts for waterlogged or excessively dry soil conditions.
- Critical Metrics at a Glance: Widgets simplify monitoring by highlighting essential metrics like soil moisture in an intuitive and accessible format.

### **View the Channel Yourself!**
You can visit this channel by going to [Public Channels on ThingSpeak](https://thingspeak.mathworks.com/channels/public). Search for the user ID: `mwa0000034847465`, and the Smart Watering System channel will be listed for access.

## **Connectivity**
This section outlines the wiring and setup for each individual sensor and the complete system. Fritzing circuit diagrams are included for visual guidance to ensure proper connections.

The following figure illustrates the Rasberry Pi 3 Model B+ Pinout:

![Raspberry Pi 3 Model B+ Pinout](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/pinout/raspberry_pi_3_pinout.png) 

### **Individual Sensor Setup**
1. Soil Moisture Sensor and MCP3008 ADC

The following figure illustrates the MCP3008 Pinout:

![MCP3008 Pinout](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/pinout/MCP3008_pinout.png) 

- MCP3008:
  - `VCC`: Connect to 3.3V on the Raspberry Pi
  - `VREF`: Connect to 3.3V on the Raspberry Pi
  - `AGND`: Connect to Ground (GND)
  - `CLK`: Connect to GPIO11/CLK
  - `MISO`: Connect to GPIO9/MISO
  - `MOSI`: Connect to GPIO10/MOSI
  - `CS`: Connect to GPIO08/CE0
  - `DGND`: Connect to Ground (GND)

- Soil Moisture Sensor:
  - `VCC`: Connect to 3.3V on the Raspberry Pi
  - `GND`: Connect to Ground (GND)
  - `AOUT`: Connect to an analog input through the MCP3008 ADC (Channel 0)

![Soil Mositure Sensor Circuit](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/circuit/soil_moisture_sensor_circuit.png) 

2. DHT22 Temperature and Humidity Sensor

The following figure illustrates the DHT22 Pinout:

![DHT22 Pinout](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/pinout/DHT22_pinout.png) 

- `VCC`: Connect to 3.3V on the Raspberry Pi
- `GND`: Connect to Ground (GND)
- `DATA`: Connect to a GPIO pin on the Raspberry Pi (e.g., GPIO17)
- A 10kΩ resistor between the VCC and DATA pins

![DHT22 Temperature and Humidity Sensor Circuit](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/circuit/DHT22_sensor_circuit.png)

3. BH1750 Light Sensor
- `VCC`: Connect to 3.3V on the Raspberry Pi
- `GND`: Connect to Ground (GND)
- `SCL`: Connect to the I2C clock pin (GPIO3/SCL)
- `SDA`: Connect to the I2C data pin (GPIO2/SDA)

![BH1750 Light Sensor Circuit](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/circuit/BH1750_sensor_circuit.png)

4. Water Pump and Relay
- `VCC`: Connect to 5V on the Raspberry Pi
- `GND`: Connect to Ground (GND)
- `IN`: Connect to a GPIO pin on the Raspberry Pi (GPIO27)
- `COM`: Connect to 5V on the Raspberry Pi
- `NO`: Connect to positive wire of the water pump
- Connect the negative wire of the water pump to the `GND`

![Water Pump and Relay Circuit](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/circuit/water_pump_circuit.png)

5. Camera
- Locate the Camera Module port
- Gently pull up on the edges of the port’s plastic clip
- Insert the Camera Module ribbon cable; make sure the connectors at the bottom of the ribbon cable are facing the contacts in the port.
- Push the plastic clip back into place

![Camera Connection](https://github.com/user-attachments/assets/881ed0da-0683-4369-a13a-9bd4613cd9f2)

### **Complete System Wiring**
The complete system integrates all the sensors, water pump, and camera, ensuring seamless data collection and automation. The consolidated wiring diagram shows the connections for all components working together:

![Water Pump and Relay Circuit](https://github.com/Gonzaleski/Smart-Watering-System/blob/main/resources/circuit/complete_circuit.png)

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
- [Raspberry Pi Foundation, Getting started with the Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/2)
- [Components101, Raspberry Pi 3 (2018)](https://components101.com/microcontrollers/raspberry-pi-3-pinout-features-datasheet)
- [MathWorks, Analyze Channel Data to Send Email Notification](https://uk.mathworks.com/help/thingspeak/analyze-channel-data-to-send-email.html)
