import pickle
import numpy as np

def load_model(filepath):
    """ Load the trained LGBM model from a pickle file. """
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model

def predict_urgency_level(model, input_features):
    """
    Predict the urgency level of a patient based on the provided input features.
    
    Args:
    model (LGBMModel): The loaded LightGBM model.
    input_features (array-like): A 1D array of features required by the model.
    
    Returns:
    int: The predicted urgency level category.
    """
    # Ensure input is in the correct shape for a single prediction
    input_features = np.array(input_features).reshape(1, -1)
    
    # Make the prediction
    prediction = model.predict(input_features)
    
    return np.argmax(prediction) 