import dlib
import cv2
import time
import os

def run_face_detection():
    detector_hog = dlib.get_frontal_face_detector()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(current_dir, "pre-trained-model", "mmod_human_face_detector.dat")

    mmod_detector = dlib.cnn_face_detection_model_v1(model_path)

    cap = cv2.VideoCapture(1)


    desired_width = 640
    desired_height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Actual Width: {actual_width}, Actual Height: {actual_height}")

    roi_x_percent, roi_y_percent = 0.3, 0.3 
    roi_w_percent, roi_h_percent = 0.4, 0.6 

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break


        frame_height, frame_width = frame.shape[:2]

        roi_x = int(frame_width * roi_x_percent)
        roi_y = int(frame_height * roi_y_percent)
        roi_w = int(frame_width * roi_w_percent)
        roi_h = int(frame_height * roi_h_percent)

  
        roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


        faces_hog = detector_hog(gray_roi)

        if len(faces_hog) == 0:
            faces_mmod = mmod_detector(gray_roi, 0)
            faces_hog = [d.rect for d in faces_mmod]

        for rect in faces_hog:
            x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
            cv2.rectangle(frame, (x + roi_x, y + roi_y), (x + w + roi_x, y + h + roi_y), (0, 255, 0), 2)


        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        cv2.imshow('Face Detection using dlib', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
