#pip install tensorflow
#pip install OpenCV

#import bytesIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import requests
import io
import json

from tensorflow.keras.utils import img_to_array
from PIL import Image
from tensorflow.keras.models import load_model

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#LOAD FROM LOCAL
app.state.model = load_model('/Users/leila/code/meloeckert/solar_project/model_multiclass_clean_damage_dirt.h5')

@app.post("/predict")
def predict(image_as_bytes):
    preprocessed_X = preprocess(image_as_bytes)
    res = predict_1(preprocessed_X)
    return res

@app.get("/")
def root():
    res = {
    'greeting': 'Hello'
}
    return res


def preprocess(images : dict):
    """
    Predict presence of damage and damage class based on image
    """
    filenames=list(images.keys())
    tile_arrays=[]
    tensors=[]
    invalid={}


    for f in filenames:
        #TODO: load image from bytes

        img = images.get(f'{f}')
        img = Image.open(io.BytesIO(img))

        try:

        #TODO image tiling
        #img_675 = img.resize((675,675))
        #tile_arrays.append(image_to_array for i in (make_tile(img)))

            img_225 = img.resize((225,225))
            tensor = img_to_array(img_225).reshape((-1, 225, 225, 3))
            tensors.append(tensor)

        except Exception as e:
            if f.lower().endswith("ds._store"):
                continue
            else:
                print("Error processing: ", f)
                print("Error: ", e)
                invalid[f]= e
                continue

    preprocessed_X = {"filenames":filenames,
                     "tensors":tensors,
                     "tile_arrays":tile_arrays,
                      "invalid":invalid
                     }

    return preprocessed_X

def find_index_of_max_element(input_list):
    max_value = max(input_list)
    max_index = input_list.index(max_value)
    return max_index

def predict_1(preprocessed_X : dict):

    res = {}

    preds = model.predict(preprocessed_X['tensors'])

    print(f"Probabilities: ")
    names_of_classes = ['clean','damaged','dirty']
    print(f"{names_of_classes}")
    print(f"{preds[0]}")
    print(f"Result: {names_of_classes[find_index_of_max_element(preds[0].tolist())]}")

    filename = preprocessed_X['filenames'][0]
    res[f'{filename}'] = names_of_classes[find_index_of_max_element(preds[0].tolist())]

    #if output != "dirt":
     #   predict_2

    res_json = json.dumps(res)
    return res_json
