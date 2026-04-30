import cv2
import os
import glob
from ultralytics import YOLO

def count_birds_yolo(folder_path, model, conf_threshold):
    image_files = glob.glob(os.path.join(folder_path, "*.*"))
    
    if not image_files:
        print("Zły folder")
        return

    for img_path in image_files:
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        results = model(img, conf=conf_threshold, verbose=False)[0]
        
        bird_count = 0
        for box in results.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            if class_name in ['bird', 'airplane', 'kite']:
                bird_count += 1
                
        filename = os.path.basename(img_path)
        print(f"{filename} -> {bird_count} ptaków (YOLO)")

if __name__ == "__main__":
    model = YOLO('yolov8n.pt')
    
    count_birds_yolo("birds_folder", model, conf_threshold=0.1)

# yolo tylko lokalizuje obiekty, nie liczy ich
# powiększanie nie dodaje szczegółów do obiektu więc nie zwiększa skuteczności YOLO