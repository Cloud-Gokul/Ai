import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0)

mask_count = 0
nomask_count = 0

# 🔥 NEW: smoothing buffer
history = []

print("Starting Mask Detection...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        if w < 100 or h < 100:
            continue

        upper_face = frame[y:y + h//2, x:x + w]
        lower_face = frame[y + h//2:y + h, x:x + w]

        upper_gray = cv2.cvtColor(upper_face, cv2.COLOR_BGR2GRAY)
        lower_gray = cv2.cvtColor(lower_face, cv2.COLOR_BGR2GRAY)

        upper_mean = upper_gray.mean()
        lower_mean = lower_gray.mean()

        diff = upper_mean - lower_mean

        # 🔥 STORE HISTORY (last 10 frames)
        history.append(diff)
        if len(history) > 10:
            history.pop(0)

        avg_diff = sum(history) / len(history)

        # 🔥 FINAL DECISION BASED ON AVERAGE
        if avg_diff > 12:
            label = "Mask"
            color = (0, 255, 0)
            mask_count += 1
            nomask_count = 0
        else:
            label = "No Mask"
            color = (0, 0, 255)
            nomask_count += 1
            mask_count = 0

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Mask Detection (Stable)", frame)

    # Exit conditions
    if mask_count >= 8:
        print("\n✅ Mask detected. Access Granted. System exiting...")
        break

    if nomask_count >= 8:
        print("\n❌ No Mask detected. Access Denied. System exiting...")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\nStopped manually")
        break

cap.release()
cv2.destroyAllWindows()