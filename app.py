from flask import Flask, render_template, Response
import cv2
from detect import process_frame

app = Flask(__name__)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not camera.isOpened():
    print("❌ Camera failed to open")
else:
    print("✅ Camera opened successfully")

def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            print("❌ Frame failed")
            continue

        frame = cv2.flip(frame, 1)  

        frame = process_frame(frame) 

        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

        if not ret:
            print("❌ Encode failed")
            continue

        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)