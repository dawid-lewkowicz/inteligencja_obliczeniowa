import cv2
import os
import glob

def count_birds_opencv(folder_path):
    image_files = glob.glob(os.path.join(folder_path, "*.*"))
    
    if not image_files:
        print("Zły folder")
        return

    for img_path in image_files:
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        bird_count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 2: 
                bird_count += 1
                
        filename = os.path.basename(img_path)
        print(f"{filename} -> {bird_count} ptaków")

if __name__ == "__main__":
    count_birds_opencv("birds_folder")