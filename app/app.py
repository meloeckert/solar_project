import streamlit as st
import requests

url = st.secrets.url

st.header("Solar panel condition classifier")
st.text("""Upload an image to evaluate the condition of solar panels.""")

# Allow users to upload images
uploaded_file = st.file_uploader("Upload an image file:", type=["jpeg", "jpg", "png"])

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    st.image(bytes_data)

    files = {"file": (bytes_data)}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        result = response.json()
        st.success("Images uploeaded succesfully!")
        st.write("API response: ", result)
    else:
        st.error("Images upload failed.")

# Evaluate images and retrieve the model's classification results
# if st.button("Evaluate"):
#     pass
