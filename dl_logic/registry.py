from params import *
from tensorflow.keras.models import Model, load_model
import glob
import os

def load_model() -> Model:

    if MODEL_TARGET == "local":

        # Get the latest model version name by the timestamp on disk
        local_model_directory = LOCAL_REGISTRY_PATH
        local_model_paths = glob.glob(f"{local_model_directory}/*")

        if not local_model_paths:
            return None

        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

        latest_model = load_model(most_recent_model_path_on_disk)

        print("Model loaded from local disk")

        return latest_model

    else:
        return None
