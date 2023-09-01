#pip install tensorflow
#pip install OpenCV

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
from io import BytesIO
import json


import numpy as np
from PIL import Image
from keras.models import load_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#LOAD FROM LOCAL
app.state.model_1 = load_model('/Users/leila/code/meloeckert/solar_project/model_multiclass_clean_damage_dirt.h5')
app.state.model_2 = load_model('/Users/leila/code/meloeckert/solar_project/model_multiclass_clean_damage_dirt.h5')

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

def preprocess(images : dict, num_tiles=3):
    """
    Predict presence of damage and damage class based on image
    """
    filenames=list(images.keys())
    tile_arrays=[]
    tensors=[]
    invalid={}

    for f in filenames:

        img = images.get(f'{f}')
        img = Image.open(BytesIO(img))

        try:

            #image tiling, array conversion; append to 'image_tiles' list
            image_tiles = []
            img_675_array = np.array(img.resize((675,675)))

            #vertical slice; num_tiles = # of equal divisions
            for v in range(0,img_675_array.shape[0],img_675_array.shape[0]//num_tiles):
                #horizontal slice; num_tiles = # of equal divisions
                for h in range(0,img_675_array.shape[1],img_675_array.shape[1]//num_tiles):
                    tile_array = img_675_array[v:v+(img_675_array.shape[0]//num_tiles), h:h+(img_675_array.shape[1]//num_tiles),:]
                    image_tiles.append(tile_array)

            tile_arrays.append(image_tiles)

            #resize full image and convert to array; append to 'tensors' list
            img_255_array = np.array(img.resize((225,225)))
            tensor = img_255_array.reshape((-1, 225, 225, 3))
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

def predict(preprocessed_X : dict):

    results = {}
    names_of_classes = ['clean','damaged','dirty']

    for x in range(len(preprocessed_X['tensors'])):
        preds = model_1.predict(preprocessed_X['tensors'][x])
        res = names_of_classes[find_index_of_max_element(preds[0].tolist())]

        if res != 'dirty':
            res = predict_2(preprocessed_X['tile_arrays'][x])

        filename = preprocessed_X['filenames'][x]
        res[f'{filename}'] = res

    results_json = json.dumps(results)
    return results_json

def predict_2(tile_arrays : dict):
    results = {}

    for t in tile_arrays:
        preds = model_2.predict(t)
        res = names_of_classes[find_index_of_max_element(preds[0].tolist())]
        results.append(res)

    #some logic to derive single result from tile results
    #if using pred probabilities, amend for-loop to append preds somewhere

    res = "tbd"
    return res
