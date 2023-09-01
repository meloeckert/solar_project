#pip install tensorflow
#pip install OpenCV

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from io import BytesIO
import json
from fastapi import File

import numpy as np
from PIL import Image
from solar_panel_status.dl_logic.registry import load_cnn_model
from solar_panel_status.dl_logic.preprocessing import preprocess
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#LOAD FROM LOCAL

app.state.model_1 = load_cnn_model()
#app.state.model_2 = load_model('solar_project/model_multiclass_clean_damage_dirt.h5')

@app.post("/predict")
def predict(image: bytes=File(...)):
    preprocessed_X = preprocess(BytesIO(image))
    res = app.state.model_1.predict(preprocessed_X)
    names_of_classes = ['clean', 'damaged','dirt']

    return {'predition': names_of_classes[find_index_of_max_element(res[0].tolist())] }


@app.get("/")
def root():
    res = {
    'greeting': 'solar project root is up'
}
    return res



def find_index_of_max_element(input_list):
    max_value = max(input_list)
    max_index = input_list.index(max_value)
    return max_index

def predict(model_1, preprocessed_X : dict):

    results = {}
    names_of_classes = ['clean','damaged','dirty']

    for x in range(len(preprocessed_X['tensors'])):
        preds = model_1.predict(preprocessed_X['tensors'][x])
        res = names_of_classes[find_index_of_max_element(preds[0].tolist())]

        # if res != 'dirty':
        #     res = predict_2(preprocessed_X['tile_arrays'][x])

        filename = preprocessed_X['filenames'][x]
        res[f'{filename}'] = res

    results_json = json.dumps(results)
    return results_json

# def predict_2(model_2, tile_arrays : dict):
#     results = {}

#     for t in tile_arrays:
#         preds = model_2.predict(t)
#         res = names_of_classes[find_index_of_max_element(preds[0].tolist())]
#         results.append(res)

#     #some logic to derive single result from tile results
#     #if using pred probabilities, amend for-loop to append preds somewhere

#     res = "tbd"
#     return res
