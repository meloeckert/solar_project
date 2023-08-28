import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import os

from PIL import Image
#from solar_project.preprocessor import preprocess_features
#from solar_project.ml_logic.registry import load_model

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#app.state.model = load_model()

#directory_path = os.path.dirname(__file__)
#file_path = os.path.join(directory_path, image_path)

image_path = random.randint(0, high=255, (3,3,3), dtype=int)

@app.get("/predict")
def predict(image_path):
    """
    Predict presence of damage and damage class based on image
    """
    #TODO url, image formats, list
    # URL of the image
    #image_url = image

    # Send an HTTP GET request to the URL
    #response = requests.get(image_url)

    # Check if the request was successful
    #if response.status_code == 200:
        # Read the content of the response (image data)
    #    image_data = response.content

        # Create a Pillow Image object from the image data
    #    image = Image.open(BytesIO(image_data))

    #else:
        #print("Failed to retrieve the image")

    #Load image from file path
    def predict(image_path):
    """
    Predict presence of damage and damage class based on image
    """
        def file_to_array(filepath):
            try:
                image = plt.imread(filepath)
                image_array=np.array(image)
                arrays.append(image_array)

            except:
                invalid.append(f)

        arrays=[]
        invalid = []
        if os.path.isdir(image_path):
            for f in os.listdir(image_path):
                filepath = os.path.join(image_path, f)
                file_to_array(filepath)

        if os.path.isfile(image_path):
            file_to_array(image_path)

        #X_processed = preprocess_features(X_df)
        #y_pred = app.state.model.predict(X_processed)

        return {'Prediction': arrays,
               'Errors': invalid}




@app.get("/")
def root():
    res = {
    'greeting': 'Hello'
}
    return res
