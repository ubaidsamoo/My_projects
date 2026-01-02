from ultralytics import YOLO
model = YOLO("fruit_best.pt")
for k, v in model.names.items():
    print(f"{k}: {v}")
