import sys
sys.path.append(r'C:\Users\abhin\Desktop\face-identification-opencv\src')
import cv2
from   fps_reading import FPSCounter
import time
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
prev_time = 0
cap = cv2.VideoCapture(0) 


while True:
    ret, frame = cap.read()
    fps_counter = FPSCounter()



    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
    
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    fps_counter.update(fps)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    cv2.imshow('Face Detection-cam1', frame)

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

