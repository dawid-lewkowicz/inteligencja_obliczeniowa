import cv2
import json
import os
from ultralytics import YOLO

def process_image(image_path, model, conf_thresholds, output_folder):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Zła nazwa pliku")
        return

    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    min_conf = min(conf_thresholds)

    results = model(image_path, conf=min_conf, verbose=False)[0]

    for current_conf in conf_thresholds:
        img_draw = img.copy()
        detections = []
        class_counts = {}

        for box in results.boxes:
            confidence = float(box.conf[0])
            
            if confidence < current_conf:
                continue 
                
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            detections.append({
                "class_name": class_name,
                "class_id": class_id,
                "confidence": round(confidence, 4),
                "bbox_xyxy": [x1, y1, x2, y2]
            })
            
            cv2.rectangle(img_draw, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img_draw, f"{class_name} {confidence:.2f}", (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        json_filename = f"{base_name}_conf_{current_conf}.json"
        json_path = os.path.join(output_folder, json_filename)
        with open(json_path, 'w') as f:
            json.dump({
                "image": image_path,
                "confidence_threshold": current_conf,
                "total_detections": len(detections),
                "class_stats": class_counts,
                "detections": detections
            }, f, indent=4)
            
        img_filename = f"{base_name}_result_with_{current_conf}_conf.jpg"
        img_path = os.path.join(output_folder, img_filename)
        cv2.imwrite(img_path, img_draw)


def process_video(video_path, model, conf_thresholds, output_folder):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Zła nazwa pliku")
        return

    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    min_conf = min(conf_thresholds)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    writers = {}
    video_data_dict = {}

    for conf in conf_thresholds:
        out_filename = f"{base_name}_result_with_{conf}_conf.mp4"
        out_path = os.path.join(output_folder, out_filename)
        writers[conf] = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
        
        video_data_dict[conf] = {
            "video_file": video_path,
            "confidence_threshold": conf,
            "tracked_ids": {},
            "frames": []
        }

    frame_idx = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, conf=min_conf, persist=True, tracker="botsort.yaml", verbose=False)[0]

        for current_conf in conf_thresholds:
            frame_draw = frame.copy()
            frame_detections = []
            
            for box in results.boxes:
                confidence = float(box.conf[0])
                
                if confidence < current_conf:
                    continue
                    
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                
                track_id = int(box.id[0]) if box.id is not None else -1 # sprawdzamy czy obiekt dostał ID od trackera

                if track_id != -1:
                    if class_name not in video_data_dict[current_conf]["tracked_ids"]:
                        video_data_dict[current_conf]["tracked_ids"][class_name] = set()
                    video_data_dict[current_conf]["tracked_ids"][class_name].add(track_id)

                frame_detections.append({
                    "class_name": class_name,
                    "track_id": track_id,
                    "confidence": round(confidence, 4),
                    "bbox_xyxy": [x1, y1, x2, y2]
                })

                cv2.rectangle(frame_draw, (x1, y1), (x2, y2), (0, 0, 255), 2)
                label = f"{class_name} ID:{track_id} {confidence:.2f}" if track_id != -1 else f"{class_name} {confidence:.2f}"
                cv2.putText(frame_draw, label, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

            video_data_dict[current_conf]["frames"].append({
                "frame_number": frame_idx,
                "detections": frame_detections
            })
            
            writers[current_conf].write(frame_draw)
            
        frame_idx += 1

    cap.release()
    
    for conf in conf_thresholds:
        writers[conf].release() 
        
        final_stats = {}
        for cls_name, ids_set in video_data_dict[conf]["tracked_ids"].items():
            final_stats[cls_name] = len(ids_set)
            
        video_data_dict[conf]["global_class_stats"] = final_stats
        del video_data_dict[conf]["tracked_ids"]
        
        json_filename = f"{base_name}_conf_{conf}.json"
        json_path = os.path.join(output_folder, json_filename)
        with open(json_path, 'w') as f:
            json.dump(video_data_dict[conf], f, indent=4)


if __name__ == "__main__":
    model = YOLO('yolov8n.pt')
    
    GLOBAL_OUTPUT_DIR = "yolo_results"
    
    image_thresholds = [0.1, 0.3, 0.5, 0.7]
    process_image('office_yolo.png', model, image_thresholds, output_folder=GLOBAL_OUTPUT_DIR)
    
    video_thresholds = [0.1, 0.5]
    process_video('office_yolo.mp4', model, video_thresholds, output_folder=GLOBAL_OUTPUT_DIR)
    process_video('street_yolo.mp4', model, video_thresholds, output_folder=GLOBAL_OUTPUT_DIR)

# wykrywa 80 klas, np. samochody, ludzi, motocykle, kot, ptak, laptop itp.
# trenował na zbiorze 300k zdjęć opisanych przez ludzi od Microsoft