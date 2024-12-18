import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from joblib import dump

# Load the data from the CSV file
data = pd.read_csv('system_data.csv')

# Prepare the features (X) and the target variable (y)
X = data[['Soil Moisture (%)', 'Temperature (°C)', 'Humidity (%)', 'Light Level (lx)']]
y = data['Valve Duration (s)']

# Scale features (Neural Networks perform better with scaled data)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data before scaling
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Train Neural Network model
mlp_model = MLPRegressor(hidden_layer_sizes=(64, 32, 16), activation='relu',
                         solver='adam', max_iter=500, random_state=42)
mlp_model.fit(X_train, y_train)

# Save the trained model
dump(mlp_model, 'model.pkl')
print("Model trained and saved successfully.")
