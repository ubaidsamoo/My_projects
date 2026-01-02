import streamlit as st
from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
import os

# ----------------------------
# 🎨 Page Configuration & UI Aesthetics
# ----------------------------
st.set_page_config(
    page_title="AI Fruit Detector",
    page_icon="🍎",
    layout="wide"
)

# Custom CSS for a premium dark mode look
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }
        .main-title {
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(45deg, #FF4B4B, #FF8E53);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            text-align: center;
            color: #A0A0A0;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3.5rem;
            background: linear-gradient(45deg, #FF4B4B, #FF8E53);
            color: white;
            font-weight: bold;
            font-size: 1.1rem;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
            color: white;
            border: none;
        }
        .result-container {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            background: #1A1C23;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🍎 AI Fruit Detection</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Scientific Magnification & Box Detection System</p>', unsafe_allow_html=True)

# ----------------------------
# 📦 Model Loading
# ----------------------------
# Mapping for fixed fruit names (Forced override for corrupted model metadata)
FRUIT_NAMES = {
    0: "Banana",
    1: "Pineapple",
    2: "Apple",
    3: "Orange",
    4: "Mango",
    5: "Grapes",
    6: "Strawberry",
    7: "Watermelon"
}

@st.cache_resource
def load_fruit_model():
    path = "fruit_best.pt" if os.path.exists("fruit_best.pt") else "yolov11n.pt"
    model = YOLO(path)
    
    # Aggressively override model.names to ensure internal consistency
    for idx, name in FRUIT_NAMES.items():
        model.names[idx] = name
        
    return model

with st.spinner("🚀 Initializing AI Vision..."):
    model = load_fruit_model()

# ----------------------------
# 📂 Image Upload & Processing
# ----------------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📤 Step 1: Upload Fruit Image")
    uploaded_file = st.file_uploader(
        "Supported formats: JPG, JPEG, PNG",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    conf_threshold = st.slider("Select Confidence Threshold", 0.05, 1.0, 0.25, 0.05)
    
    if uploaded_file:
        input_image = Image.open(uploaded_file).convert("RGB")
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.image(input_image, caption="Original Image", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        detect_btn = st.button("🔍 START SCAN")

with col2:
    st.markdown("### 🎯 Step 2: Detection Result")
    if uploaded_file and detect_btn:
        with st.spinner("🧠 Analyzing Fruit Samples..."):
            # Prepare image
            img_np = np.array(input_image)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            
            # Run inference
            results = model(img_bgr, conf=conf_threshold, imgsz=640)
            
            detections_found = False
            all_detected_labels = []
            output_img = img_bgr.copy()
            detection_count = 0
            
            # Colors for different classes to match the "Look" the user wants
            # Using high-contrast premium colors
            CLASS_COLORS = {
                0: (255, 100, 0),   # Banana (Blue-ish/Orange Mix)
                1: (255, 255, 0),   # Pineapple (Cyan)
                2: (0, 0, 255),     # Apple (Red)
                3: (0, 165, 255),   # Orange (Orange Color)
                4: (0, 255, 255),   # Mango (Yellow)
                5: (255, 0, 255),   # Grapes (Pink/Purple)
            }
            DEFAULT_COLOR = (0, 255, 0) # Green for others

            # Processing results
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    # Use our fixed mapping exclusively to avoid metadata strings
                    label = FRUIT_NAMES.get(cls_id, f"Fruit {cls_id}")
                    conf = float(box.conf[0])
                    
                    # Skip if the label is accidentally the metadata string (protection)
                    if "dataset" in label.lower() or "created on" in label.lower():
                        continue

                    detections_found = True
                    detection_count += 1
                    all_detected_labels.append(label)
                    
                    # Coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Style: Box color based on class
                    color = CLASS_COLORS.get(cls_id, DEFAULT_COLOR)
                    
                    # Draw Bounding Box (Scientific Rounded Corners style)
                    cv2.rectangle(output_img, (x1, y1), (x2, y2), color, 2)
                    
                    # Draw Label Tag (Background for readability)
                    label_txt = f"{label} {int(conf*100)}%"
                    (tw, th), _ = cv2.getTextSize(label_txt, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    cv2.rectangle(output_img, (x1, y1 - th - 10), (x1 + tw + 10, y1), color, -1)
                    cv2.putText(output_img, label_txt, (x1 + 5, y1 - 7), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

                    # Magnification Zoom View (Top layer)
                    try:
                        crop = img_bgr[y1:y2, x1:x2]
                        if crop.size > 0 and detection_count <= 4: # Limit zoom windows to 4
                            zoom_size = 150
                            zoom_view = cv2.resize(crop, (zoom_size, zoom_size))
                            cv2.rectangle(zoom_view, (0, 0), (zoom_size-1, zoom_size-1), color, 3)
                            
                            h, w, _ = img_bgr.shape
                            # Placement logic to avoid overlapping
                            z_x = w - zoom_size - 20
                            z_y = 20 + (detection_count-1) * (zoom_size + 20)
                            
                            if z_y + zoom_size < h:
                                output_img[z_y:z_y+zoom_size, z_x:z_x+zoom_size] = zoom_view
                                cv2.putText(output_img, f"SCAN #{detection_count}", (z_x, z_y - 5), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                                # Thin line connecting box to zoom
                                cv2.line(output_img, (x2, y1), (z_x, z_y), color, 1)
                    except Exception:
                        pass

            if detections_found:
                st.success(f"✅  Scan Complete! {len(all_detected_labels)} fruits identified.")
                result_rgb = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.image(result_rgb, caption="AI Identification & Magnification View", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show summary in a nice grid
                st.markdown("### 📊 Detection Intelligence Summary")
                cols = st.columns(3)
                for i, lbl in enumerate(all_detected_labels):
                    with cols[i % 3]:
                        st.info(f"📍 Item {i+1}: **{lbl.upper()}**")
            else:
                st.warning("⚠️ No fruit samples identified in this scan. Try lowering the confidence threshold.")
                st.image(input_image, use_container_width=True)
    else:
        st.info("💡 Pro Tip: Upload an image of Mixed Fruits (Apple, Banana, Mango) for the best results.")

# ----------------------------
# 📌 Footer
# ----------------------------
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#666;">YOLO11 Fruit Intelligence System v3.0 | Optimized for FRUITS DETECTION</p>', 
    unsafe_allow_html=True
)
