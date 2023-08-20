import sys
sys.path.append(r'C:\Users\abhin\Desktop\face-identification-opencv\src')
import cv2
import time
import dlib
from fps_reading import FPSCounter

print(dlib.DLIB_USE_CUDA)
if dlib.DLIB_USE_CUDA:
    print("DLIB is using CUDA!")
else:
    print("DLIB is NOT using CUDA.")

mmod_detector = dlib.cnn_face_detection_model_v1("../pre-trained-model/mmod_human_face_detector.dat")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
prev_time = 0
fps_counter = FPSCounter()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = mmod_detector(gray)
    for rect in faces:
        x, y, w, h = rect.rect.left(), rect.rect.top(), rect.rect.width(), rect.rect.height()
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    fps_counter.update(fps)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Face Detection using dlib-MMOD', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        average_fps = fps_counter.get_average_fps()
        lowest_fps = fps_counter.get_lowest_fps()
        highest_fps = fps_counter.get_highest_fps()
        print(f"Average FPS for the session: {average_fps:.2f}")
        print(f"Lowest FPS during the session: {lowest_fps:.2f}")
        print(f"Highest FPS during the session: {highest_fps:.2f}")
        break

cap.release()
cv2.destroyAllWindows()
