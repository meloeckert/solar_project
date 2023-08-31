import os


########## VARIABLES #########
MODEL_TARGET = "local"  #to target .env, just use instead: os.environ.get("MODEL_TARGET")



######### CONSTANTS #########
LOCAL_REGISTRY_PATH =  os.path.join(os.getcwd(), "models")
