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
    page_title="Helmet Detection",
    page_icon="🪖",
    layout="centered"
)

st.title("🪖 Helmet / No Helmet Detection")
st.write("Upload an image to detect **Helmet** or **No Helmet**")

# ---------------------------
# Load YOLO Model
# ---------------------------
MODEL_PATH = "helmet_best.pt"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        # Fallback to best.pt if helmet_best.pt is missing
        if os.path.exists("best.pt"):
            return YOLO("best.pt")
        st.error(f"❌ '{MODEL_PATH}' model file is missing!")
        st.stop()
    return YOLO(MODEL_PATH)

model = load_model()

# ---------------------------
# Image Upload
# ---------------------------
uploaded_file = st.file_uploader(
    "📤 Upload an image to detect helmet",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        # Open the uploaded image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Detect Helmet"):
            with st.spinner("Detecting Helmet..."):
                # Convert the uploaded image to numpy array (RGB)
                img_np = np.array(image)
                
                # Run YOLO model for detection
                results = model(img_np, conf=0.4)

                # Create a copy for custom drawing
                annotated_img = img_np.copy()

                # Process each detection
                for result in results[0].boxes:
                    # Get coordinates, class, and confidence
                    x1, y1, x2, y2 = map(int, result.xyxy[0])
                    cls_id = int(result.cls[0])
                    conf = float(result.conf[0])
                    label_name = model.names[cls_id]
                    
                    # Define colors based on class (in RGB)
                    # "Helmet" -> Cyan (0, 255, 255)
                    # "No_helmet" -> Red (255, 0, 0)
                    if "no" in label_name.lower():
                        box_color = (255, 0, 0)  # Red
                        text_color = (255, 255, 255)
                    else:
                        box_color = (0, 255, 255) # Cyan
                        text_color = (0, 0, 0)

                    # 1. Draw Bounding Box
                    cv2.rectangle(annotated_img, (x1, y1), (x2, y2), box_color, 3)

                    # 2. Draw Label Background (Filled box)
                    label_text = f"{label_name.replace('_', ' ')} {conf:.2f}"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.8
                    thickness = 2
                    (text_w, text_h), baseline = cv2.getTextSize(label_text, font, font_scale, thickness)
                    
                    # Ensure label background is within image bounds
                    bg_y1 = max(0, y1 - text_h - 10)
                    cv2.rectangle(annotated_img, (x1, bg_y1), (x1 + text_h + text_w, y1), box_color, -1)

                    # 3. Draw Label Text
                    cv2.putText(annotated_img, label_text, (x1 + 5, y1 - 7), 
                                font, font_scale, text_color, thickness)

            # Show the result with annotated image
            st.success("✅ Detection Complete")
            st.image(
                annotated_img,
                caption="Helmet Detection Result",
                use_container_width=True
            )

    except Exception as e:
        st.error("❌ Error processing the image")
        st.code(str(e))
