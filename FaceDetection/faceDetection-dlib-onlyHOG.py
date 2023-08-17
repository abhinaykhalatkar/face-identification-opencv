
import cv2
import time
import dlib
print(dlib.DLIB_USE_CUDA)
if dlib.DLIB_USE_CUDA:
    print("DLIB is using CUDA!")
else:
    print("DLIB is NOT using CUDA.")

detector = dlib.get_frontal_face_detector()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for rect in faces:
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with detected faces and FPS
    cv2.imshow('Face Detection using dlib-hog', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()