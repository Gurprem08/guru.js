# ml_model.py

import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler



def predict(parameters):
    target_features = ['CO3', 'Cl', 'SO4', 'TH', 'Ca', 'Mg', 'Na']
# Load the models for prediction
    loaded_models = {target: joblib.load(f'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\model_{target}.pkl') for target in target_features}

    # Load the fitted scaler
    scaler = joblib.load('scaler.pkl')
    
    parameters = np.array(parameters).reshape(1, -1)
    parameters = scaler.transform(parameters)  # Normalize the input parameters
    predictions = {}

    for target, model in loaded_models.items():
        predictions[target] = model.predict(parameters)[0]

    return predictions

