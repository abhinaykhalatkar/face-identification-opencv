import cv2
import time
from .detectors import initialize, roi, face_detection, display

def run_face_detection():
    detector_hog, mmod_detector = initialize.initialize_detectors()
    cap = cv2.VideoCapture(0)

    desired_width = 640
    desired_height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,cv2.CAP_PROP_FRAME_WIDTH)
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Actual Width: {actual_width}, Actual Height: {actual_height}")

    roi_x_percent, roi_y_percent = 0.2, 0.05
    roi_w_percent, roi_h_percent = 0.5, 0.6 

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
        cv2.putText(frame, f"{fps:.2f}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow('Face Detection using dlib', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()