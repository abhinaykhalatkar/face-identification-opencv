import cv2
import time
from collections import deque
from .detectors import initialize, face_detection, display
from fps_reading import FPSCounter

def run_face_detection():
    fps_counter = FPSCounter()
    detector_hog, mmod_detector = initialize.initialize_detectors()
    cap = cv2.VideoCapture(0)
    detection_history = deque(maxlen=5)  ##5frames average ,best of 4
    
    reset_interval = 2
    start_time = time.time()
    buffer_percentage = 0.1

    frame_height, frame_width = cap.read()[1].shape[:2]
    roi_x, roi_y = 0, 0
    roi_w, roi_h = frame_width, frame_height

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        elapsed_time = time.time() - start_time

        roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        faces_hog = face_detection.detect_faces(roi_frame, detector_hog, mmod_detector)
        detection_history.append(1 if len(faces_hog) > 0 else 0)

        if sum(detection_history) >= 4 and len(faces_hog) > 0:
            sorted_faces = sorted(faces_hog, key=lambda rect: rect.top())  # Sort by topmost point
            first_face = sorted_faces[0]
            last_face = sorted_faces[-1]

            buffer_w = int(buffer_percentage * frame_width)
            buffer_h = int(buffer_percentage * frame_height)

            # Adjust the roi_x and roi_y values to be relative to the full frame
            roi_x = max(0, roi_x + first_face.left() - buffer_w)
            roi_y = max(0, roi_y + first_face.top() - buffer_h)
            roi_w = min(frame_width - roi_x, (last_face.right() - first_face.left()) + 2 * buffer_w)
            roi_h = min(frame_height - roi_y, (last_face.bottom() - first_face.top()) + 2 * buffer_h)
        # ...
        # Reset the ROI every reset_interval seconds
        if elapsed_time > reset_interval:
            roi_x, roi_y = 0, 0
            roi_w, roi_h = frame_width, frame_height
            start_time = time.time()  # Reset the start time

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
