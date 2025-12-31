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
    page_title="License Plate Detection",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 License Plate Detection")
st.write("Upload an image to detect **Vehicle License Plate**")

# ---------------------------
# Load Model (Local + Cloud Safe)
# ---------------------------
MODEL_PATH = "license_best.pt"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error("❌ license_best.pt file not find in  project folder ")
        st.stop()
    return YOLO(MODEL_PATH)

model = load_model()

# ---------------------------
# Upload Image
# ---------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Vehicle Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Detect License Plate"):
            with st.spinner("Detecting License Plate..."):
                img = np.array(image)

                results = model(img, conf=0.4)

                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = model.names[cls_id]  # usually: license_plate

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    color = (0, 255, 0)
                    text = f"{label} {conf:.2f}"

                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        img,
                        text,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2
                    )

            st.success("✅ Detection Complete")
            st.image(img, caption="License Plate Detection Result", use_container_width=True)

    except Exception as e:
        st.error("❌ Image process  error ")
        st.code(str(e))
