from ultralytics import YOLO
import cv2
import os

model = YOLO("fruit_best.pt")
print("Model Names:", model.names)

# The image path from metadata
image_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\6cf996c9-6887-4724-be4c-f480ee88784d\uploaded_image_1767370892106.jpg"

if os.path.exists(image_path):
    results = model(image_path)
    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            print(f"Detected class {cls} ({model.names[cls]}) with confidence {conf:.2f}")
else:
    print("Image not found at path:", image_path)
