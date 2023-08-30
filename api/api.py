import pandas as pd
import numpy as np

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import os

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

def convert_to_jpeg(filepath):
        #Load image
        img= Image.open(filepath)

        # Convert the image to RGB mode
        img = img.convert("RGB")

        # Save the image in JPEG format as <original filepath>.jpeg to the "jpeg_tmp" folder
        name = os.path.basename(filepath).replace("jpg", "jpeg")
        new_filepath = os.path.join(os.getcwd(), "jpeg_tmp", name)
        img.save(new_filepath, "JPEG")

        # Close the image to free resources
        img.close()

        return new_filepath

def file_to_arrays_list(filepath):
        '''Converts JPEG files to arrays and appends arrays & filenames to 'arrays' & 'filenames' lists
        Appends filenames of unprocessible files to 'invalid' list'''

        image= Image.open(filepath)
        image_array=np.array(image)
        arrays.append(image_array)
        return arrays

def process_filepath(filepath):
    filepaths = []
    arrays=[]
    invalid = []

    #Gets file paths for input files
    for root, dirs, files in os.walk(image_path):
        for file in files:
            filepath = os.path.join(root, file)
            #Ignores macOS hidden system file in directories
            if filepath.lower().endswith(".ds_store"):
                continue

            try:
                #Converts JPEG files to arrays and add filepath to 'filepaths' list
                if file.lower().endswith(".jpeg"):
                    file_to_arrays_list(filepath)
                    filepaths.append(filepath)

                #Processes non-JPEG image files, converts to arrays and adds original image filepath to 'filepaths' list
                else:
                    #Creates jpeg_tmp for converted images if not already created
                    if not os.path.exists(os.path.join(os.getcwd(), "jpeg_tmp")):
                            os.makedirs(os.path.join(os.getcwd(), "jpeg_tmp"))

                    #Save JPEG to jpeg_tmp with original filepath as name
                    original_filepath=filepath
                    filepath = convert_to_jpeg(filepath)

                    #Converts JPEGs to arrays and adds original image filepath to 'filepaths' list
                    file_to_arrays_list(filepath)
                    filepaths.append(original_filepath)
                    os.remove(filepath)

            except Exception as e:
                    print("Error processing:", filepath)
                    print("Error:", e)
                    invalid.append(filepath)

    return {
        'array_filepaths':filepaths,
        'arrays': arrays,
        'invalid_filepaths': invalid
        }


@app.post("/predict")
def predict(image_path):
    """
    Predict presence of damage and damage class based on image
    """
    predictions=[]

    arrays = process_filepath(image_path)['arrays']
    for a in arrays:
        pred = model.predict(a)
        predictions.append(pred)
    #filepath/predictions zip

    return f"Predictive wizardry for {image_path} coming soon..."

    #


@app.get("/")
def root():
    res = {
    'greeting': 'Hello'
}
    return res
