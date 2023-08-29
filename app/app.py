import streamlit as st
import numpy as np
import pandas as pd

st.header("Solar panel condition classifier")
st.text("""Upload an image to evaluate the condition of solar panels.""")

# Allow users to upload images
uploaded_file = st.file_uploader("Upload an image file:", )

# Evaluate images and retrieve the model's classification results
st.button("Evaluate")
