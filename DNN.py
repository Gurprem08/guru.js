import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Dropout # type: ignore
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error , r2_score
import joblib

# Load the dataset
data = pd.read_csv('f_dataset.csv')

# Basic parameters used as input
input_features = ["pH", "EC", "TDS", "Temperature"]

# Target parameters to predict
target_features = ['CO3','Cl', 'SO4','TH', 'Ca', 'Mg', 'Na']

# Splitting data into input and target variables
X = data[input_features]
y = data[target_features]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

joblib.dump(scaler, 'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\scaler.pkl')

# Define the DNN model
def create_dnn_model(input_dim):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dropout(0.2))  # 20% dropout
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))  # 20% dropout
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.3))  # 30% dropout
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.3))  # 30% dropout
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.2))  # 20% dropout
    model.add(Dense(1))  # Output layer with 1 neuron
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Dictionary to hold the models and their predictions
models = {}
predictions = {}
results = {}
r2_results ={}

# Train and evaluate a separate model for each target parameter
for target in target_features:
    print(f'Training model for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]
    
    model = create_dnn_model(input_dim=X_train.shape[1])
    history = model.fit(X_train, y_target_train, epochs=100, batch_size=32, validation_split=0.2, verbose=0)
    
    models[target] = model
    y_pred = model.predict(X_test)
    predictions[target] = y_pred
    results[target] = model.evaluate(X_test, y_target_test)
    joblib.dump(model, f'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\model_{target}.pkl')

