import sys
sys.path.append(r'C:\Users\abhin\Desktop\face-identification-opencv\src')
import cv2
import time
from FaceDetection.detectors import initialize, roi, face_detection, display
from fps_reading import FPSCounter

detector_hog, mmod_detector = initialize.initialize_detectors()
cap = cv2.VideoCapture(0)
fps_counter = FPSCounter()
    

    # desired_width = 640
    # desired_height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,cv2.CAP_PROP_FRAME_WIDTH)
    # actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print(f"Actual Width: {actual_width}, Actual Height: {actual_height}")

roi_x_percent, roi_y_percent = 0, 0
roi_w_percent, roi_h_percent = 1, 1 

prev_time = 0

while True:
        ret, frame = cap.read()
        if not ret:
            break

        roi_frame, roi_x, roi_y, roi_w, roi_h = roi.get_roi(frame, roi_x_percent, roi_y_percent, roi_w_percent, roi_h_percent)
        faces_hog = face_detection.detect_faces(roi_frame, detector_hog, mmod_detector)
        frame = display.display_results(frame, faces_hog, roi_x, roi_y, roi_w, roi_h) 

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        fps_counter.update(fps)
        cv2.putText(frame, f"{fps:.2f}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow('Face Detection using dlib', frame)

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
