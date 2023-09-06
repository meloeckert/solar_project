#from params import *
from tensorflow.keras.models import Model, load_model
#import glob
import os

def load_cnn_model(MODEL_TARGET='local') -> Model:
    if MODEL_TARGET == "local":
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Get the latest model version name by the timestamp on disk
        local_model_path = os.path.join(current_dir,'..','models','model_multiclass_clean_damage_dirt_230904_statusquo.h5')

        if not local_model_path:
            return None


        latest_model = load_model(local_model_path)

        print("Model loaded from local disk")

        return latest_model

    else:
        return None
