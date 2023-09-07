import streamlit as st
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

# Load known face encodings and names
def load_known_faces():
    amit_shah_image = face_recognition.load_image_file("photos/amitshah.jpg")
    amit_shah_encoding = face_recognition.face_encodings(amit_shah_image)[0]
    bill_gates_image = face_recognition.load_image_file("photos/billgates.jpg")
    bill_gates_encoding = face_recognition.face_encodings(bill_gates_image)[0]
    # ... Load encodings and names for other individuals ...

    known_face_encoding = [
        amit_shah_encoding,
        bill_gates_encoding,
        # ... Add encodings for other individuals ...
    ]

    known_face_names = [
        "Amit shah",
        "Bill gates",
        # ... Add names for other individuals ...
    ]

    return known_face_encoding, known_face_names

known_face_encoding, known_face_names = load_known_faces()
students = known_face_names.copy()
face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
csv_filename = f"{current_date}.csv"
f = open(csv_filename, "w+", newline="")
lnwriter = csv.writer(f)

video_capture = cv2.VideoCapture(0)

st.title("Attendance System")

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            if name in known_face_names:
                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name, current_time])

    st.image(frame, caption="Attendence_System", use_column_width=True)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
