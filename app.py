import pandas as pd
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
with open("finalized_model.sav", "rb") as f:
    model = pickle.load(f)

# Load the training features
with open("feature_names.pkl", "rb") as f:
    training_features = pickle.load(f)
    print (training_features)

# Function to preprocess the input data
def preprocess_data(input_data):
    # Define your feature names
    feature_names = [
    'Tumor Margin',
    'more than 50% exophytic, under 50% exophytic, or entirely endophytic?',
    'Renal Sinus',
    'Medial/lateral rim', 
    'Sinus/Polar Line',
    'T2 Intensity',
    'Solid/Cystic',
    '% Enhancement (T1 nephrographic phase)',
    'T1 Enhancement (Corticomedullary Phase)',
    'T1 Enhancement (Nephrographic Phase)', 
    'T1 Enhancement (Excretory Phase)',
    'Diffusion Restriction'
     ] 
    
    # Preprocess the input data
    data = pd.DataFrame([input_data], columns=feature_names)
    
    data = data.fillna('')

    # One-hot encode each feature separately
    one_hot_data = pd.get_dummies(data, columns=feature_names)
    print (one_hot_data)
    
    # Return one-hot encoded data
    return one_hot_data

# Function to align input data features with training data features, think about this function dude! :D 
def align_features(input_data, training_features):
    # Add missing columns with all values set to 0
    for column in training_features:
        if column not in input_data.columns:
            input_data[column] = 0

    # Order the columns to match training data
    input_data = input_data[training_features]

    return input_data

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print(data)
    
    # Preprocess and align the input data
    preprocessed_data = preprocess_data(data['input'])
    aligned_data = align_features(preprocessed_data, training_features)
    
    # Save preprocessed data for verification
    aligned_data = aligned_data.astype(int)
    aligned_data.to_csv('aligned_data.csv', index=False)

    # Make a prediction
    prediction = model.predict(aligned_data)

    # Return the prediction as a JSON response
    response = {'prediction': int(prediction[0])}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
