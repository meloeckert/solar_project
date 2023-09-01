# Import necessary and useful libraries
import numpy as np
import pandas as pd

from tensorflow.keras import models, layers, optimizers, callbacks, Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf


# Create a function that initializes our CNN Model without (!!) compiling it.
def initialize_cnn_model(input_shape: tuple) -> Model:

    model = Sequential()

    # Change the scale of colors from (0,255) to (0,1)
    model.add(layers.Rescaling(1./255, input_shape=input_shape))

    # Add data augmentation layers
    model.add(layers.RandomFlip("horizontal"))
    model.add(layers.RandomZoom(0.1))
    model.add(layers.RandomTranslation(0.2, 0.2))
    model.add(layers.RandomRotation(0.1))

    # Add Convolutional Layers
    model.add(layers.Conv2D(filters = 32, kernel_size = (3,3), activation="relu", padding = "same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), padding = "same") )

    model.add(layers.Conv2D(filters = 32, kernel_size = (3,3), activation="relu", padding = "same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), padding = "same"))

    model.add(layers.Conv2D(filters = 64, kernel_size = (3,3), activation="relu", padding = "same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), padding = "same"))

    model.add(layers.Conv2D(filters = 128, kernel_size = (3,3), activation="relu", padding = "same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), padding = "same") )

    # Flattening
    model.add(layers.Flatten())

    # Add Dense layers and a final predictive layer suiteable for the task
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dropout(0.5))

    model.add(layers.Dense(3, activation="softmax"))

    print("Model initialized")

    return model


# Create a function that compiles the model that we built by using 'initialize_cnn_model'
def compile_model(model: Model, learning_rate=0.001) -> Model:

    adam = optimizers.Adam(learning_rate=learning_rate)

    model.compile(loss= SparseCategoricalCrossentropy(),
              optimizer= adam,
              metrics=['accuracy'])

    print("Model compiled")

    return model


# Train the model
def train_model(
    model: Model,
    x: tf.data.Dataset,
    epochs=100,
    batch_size=16,
    validation_data=None, # Overrides validation_split if specified
    validation_split=0.2,
    patience=10,
    class_weight=None
) -> tuple[Model, dict]:

    es = EarlyStopping(
        monitor="val_loss",
        patience=patience,
        restore_best_weights=True,
        verbose=1)

    history = model.fit(
        x,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=validation_data,
        validation_split=validation_split,
        callbacks=[es],
        verbose=0,
        class_weight=class_weight
    )

    print("Model trained")

    return model, history


# Evaluate the trained model
def evaluate_model(
    model: Model,
    x: tf.data.Dataset,
    batch_size=16
) -> tuple[Model, dict]:

    print("Evaluating model...")

    if Model is None:
        print("Error: No model to evaluate!")
        return None

    metrics = model.evaluate(
        x,
        batch_size=batch_size,
        verbose=0,
        return_dict=True)

    print("Model evaluated")

    return Model, metrics
