import cv2
import face_recognition
import pickle
import os

def generate_encodings(image_folder, save_path='encodings.pickle'):
    known_encodings = []
    known_names = []

    print("[INFO] Encoding faces... please wait.")
    
    for filename in os.listdir(image_folder):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            # Load image and get name from filename
            path = os.path.join(image_folder, filename)
            name = os.path.splitext(filename)[0]
            
            image = cv2.imread(path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detect face locations and encodings
            boxes = face_recognition.face_locations(rgb_image, model='hog')
            encodings = face_recognition.face_encodings(rgb_image, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)
                print(f"[SUCCESS] Encoded: {name}")

    # Save encodings to a file
    data = {"encodings": known_encodings, "names": known_names}
    with open(save_path, "wb") as f:
        f.write(pickle.dumps(data))
    
    print(f"[INFO] Saved {len(known_names)} encodings to {save_path}")

if __name__ == "__main__":
    # Ensure you have a folder named 'images' with photos in it
    generate_encodings('images')
