from django.shortcuts import render
import pickle
import os
from django.conf import settings
from django.http import JsonResponse
import numpy as np
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import Ridge


# Helper function to load Ridge model
def load_ridge_model():
    # Define the path to the Ridge model pickle file
    pickle_file_path = os.path.join(settings.MEDIA_ROOT, 'ridge.pkl')

    try:
        with open(pickle_file_path, 'rb') as file:
            ridge_model = pickle.load(file)
        return ridge_model
    except FileNotFoundError:
        raise Exception("Ridge model file not found!")
    except pickle.UnpicklingError:
        raise Exception("Error unpickling Ridge model!")


# Helper function to load Standard Scaler model
def load_standard_scaler():
    # Define the path to the Standard Scaler pickle file
    pickle_file_path = os.path.join(settings.MEDIA_ROOT,'scaler.pkl')

    try:
        with open(pickle_file_path, 'rb') as file:
            scaler = pickle.load(file)
        return scaler
    except FileNotFoundError:
        print(pickle_file_path)
        raise Exception("Standard Scaler file not found!"+pickle_file_path)
    except pickle.UnpicklingError:
        raise Exception("Error unpickling Standard Scaler!")


# View for prediction
def predict(request):
    if request.method == "POST":
        data = request.POST

        # Get form input values
        Temperature = float(data.get('Temperature'))
        RH = float(data.get('RH'))
        Ws = float(data.get('Ws'))
        Rain =float(data.get('Rain'))
        FFMC = float(data.get('FFMC'))
        DMC = float(data.get('DMC'))
        ISI = float(data.get('ISI'))
        Classes = float(data.get('Classes'))
        Region = float(data.get('Region'))

        # Collect all inputs into an array for transformation
        #'Temperature', 'RH', 'Ws', 'Rain', 'FFMC', 'DMC', 'ISI', 'Classes','Region'
        det = [[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]]
       

        # Load the scaler and model
        try:
            scaler = load_standard_scaler()
            ridge_model = load_ridge_model()
           
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        # Scale the input data
        try:
            new_data_scaled = scaler.transform(det)
            
        except Exception as e:
            return JsonResponse({"error": f"Scaling error: {str(e)}"}, status=500)

        # Make a prediction using the ridge model
        try:
            result = ridge_model.predict(new_data_scaled)
           
        except Exception as e:
            return JsonResponse({"error": f"Prediction error: {str(e)}"}, status=500)

        # Render the result in the template
        return render(request, 'fire_forcast.html', {'results': result[0]})

    else:
        return render(request, 'fire_forcast.html')