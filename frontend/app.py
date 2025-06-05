import streamlit as st
from PIL import Image
import requests
import io
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.generate_stl import convert_sketch_to_stl

# Title
st.set_page_config(layout="centered")
st.title("🧱 Clay 3D Printer – Sketch to Print")

st.markdown("Transform your 2D sketches into printable 3D clay models for the Plotterbot!")

# Step 1 – Draw or Upload Image
st.header("✏️ Step 1: Input – Draw or Upload")
input_method = st.radio("Choose input method:", ["Draw on Canvas", "Upload Image"])

uploaded_image = None

if input_method == "Upload Image":
    uploaded_image = st.file_uploader("Upload a PNG/JPG of your sketch", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Sketch", width=300)

# Step 2 – Process to 3D
st.header("🧱 Step 2: Process Sketch into 3D")

if st.button("🌀 Generate 3D Model"):
    if uploaded_image:
        # Send image to backend for STL generation
        image_bytes = uploaded_image.getvalue()
        stl_data = convert_sketch_to_stl(image_bytes)

        # Show success and provide STL download
        st.success("3D model generated successfully!")
        st.download_button("⬇️ Download STL", data=stl_data, file_name="model.stl")
    else:
        st.warning("Please upload a sketch image first.")