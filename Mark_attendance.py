import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime

def log_attendance(name):
    with open('attendance_list.csv', 'r+') as f:
        data_list = f.readlines()
        names = [line.split(',')[0] for line in data_list]
        
        if name not in names:
            now = datetime.now()
            time_string = now.strftime('%H:%M:%S')
            date_string = now.strftime('%Y-%m-%d')
            f.writelines(f'\n{name},{date_string},{time_string}')
            print(f"[LOG] Attendance marked for: {name}")

# 1. Load the trained data
print("[INFO] Loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

# 2. Initialize Webcam
video_capture = cv2.VideoCapture(0)

print("[INFO] Starting webcam. Press 'q' to exit.")

while True:
    ret, frame = video_capture.read()
    # Scale down frame for faster processing (0.25 size)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Find faces in current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare face with known encodings
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = data["names"][best_match_index]
            log_attendance(name)

        # Rescale coordinates back to original size for drawing
        top, right, bottom, left = top*4, right*4, bottom*4, left*4
        
        # Draw Box and Label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow('Attendance System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
