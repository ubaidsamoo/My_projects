from ultralytics import YOLO
import os

path = "fruit_best.pt" if os.path.exists("fruit_best.pt") else "yolov8n.pt"
model = YOLO(path)
print(model.names)
