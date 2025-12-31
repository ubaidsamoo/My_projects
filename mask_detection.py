import streamlit as st
from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
import os

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Mask Detection",
    page_icon="😷",
    layout="centered"
)

st.title("😷 Mask / No Mask Detection")
st.write("Upload an image and the model will detect **Mask** or **No Mask**")

# ---------------------------
# Load Model (Safe way)
# ---------------------------
MODEL_PATH = "best.pt"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error("❌ best.pt file nahi mili! Please same folder me rakho.")
        st.stop()
    return YOLO(MODEL_PATH)

model = load_model()

# ---------------------------
# Image Upload
# ---------------------------
uploaded_file = st.file_uploader(
    "📤 Image upload karo",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Detect Mask"):
            with st.spinner("Detecting..."):
                img_np = np.array(image)
                results = model(img_np, conf=0.4)

                annotated_img = results[0].plot()
                annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

            st.success("✅ Detection Complete")
            st.image(annotated_img, caption="Detection Result", use_container_width=True)

    except Exception as e:
        st.error("❌ Image process karte waqt error aaya")
        st.code(str(e))
