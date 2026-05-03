import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("mask_model.h5")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def process_frame(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        print("Faces:",len(faces))

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]

            if face.size == 0:
                continue

            face = cv2.resize(face, (128, 128))
            face = face / 255.0
            face = np.reshape(face, (1, 128, 128, 3))

            pred = model.predict(face, verbose=0)
            label_index = pred.argmax()

            if label_index == 0:
                label = "Mask"
                color = (0,255,0)
            else:
                label = "No Mask"
                color = (0,0,255)

            cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
            cv2.putText(frame, label, (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        return frame

    except Exception as e:
        print("❌ Error in process_frame:", e)
        return frame