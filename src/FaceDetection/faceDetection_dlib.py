import sys
sys.path.append('C:/Users/abhin/Desktop/face-identification-opencv/src')
import cv2
import time
import pickle
import dlib
import numpy as np
from collections import deque
from .detectors import initialize, face_detection, display
from fps_reading import FPSCounter
# from UI.face_capture_ui import open_face_capture_window
from PIL import Image, ImageTk
import tkinter as tk
import os
from UI.face_capture_ui import open_face_capture_window

with open("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/embeddings.pkl", "rb") as f:
    saved_embeddings, saved_labels = pickle.load(f)
    
face_rec_model_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/dlib_face_recognition_resnet_model_v1.dat"
shape_predictor_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/shape_predictor_68_face_landmarks.dat"
print(dlib.__version__)
sp = None
facerec = None
all_windows_closed = False
add_person_clicked = False
exit_requested = False
user_Names_for_oneNote= []
is_namelist_requested=False
user_celar_requested=False

def add_to_user_Names_for_oneNote(new_string):
    if new_string not in user_Names_for_oneNote and 'unknown' not in new_string.lower():
        user_Names_for_oneNote.append(new_string)


def initialize_dlib_models():
    global sp, facerec
    sp = dlib.shape_predictor(shape_predictor_path)
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)

def identify_face(face_descriptor, saved_embeddings, saved_labels, threshold=0.5):
    distances = [np.linalg.norm(np.array(face_descriptor) - np.array(embedding)) for embedding in saved_embeddings]
    min_distance_index = np.argmin(distances)
    if distances[min_distance_index] < threshold:
        return saved_labels[min_distance_index]
    else:
        return "Unknown"

def on_add_person_click():
    global add_person_clicked
    add_person_clicked = True

def handle_key_press(event):
    global is_namelist_requested
    global exit_requested
    global user_celar_requested
    if event.char == 'q':
       exit_requested = True
    elif event.char == 'w':
        is_namelist_requested = True
    elif event.char == 'c':
        user_celar_requested = True
    
    
def capture_face_and_save(detector, cap):
    start_time = time.time()
    captured_images = []


    while time.time() - start_time < 3: 
        ret, frame = cap.read()
        if not ret:
            break
        print('while')
        detected_faces = face_detection.detect_faces(frame, detector)
        for face in detected_faces:
            x, y, w, h = (face.left(), face.top(), face.width(), face.height())
            cropped_face = frame[y:y+h, x:x+w]
            captured_images.append(cropped_face)
            print('for')

        cv2.imshow('Capturing Face', frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    return captured_images

def save_captured_images(name, images):
    save_path = f"C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/{name}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for idx, img in enumerate(images):
        cv2.imwrite(os.path.join(save_path, f"{name}_{idx}.jpg"), img)

def run_face_detection(video_canvas,root):
    global all_windows_closed
    global is_namelist_requested
    global user_celar_requested
    initialize_dlib_models()
    fps_counter = FPSCounter()
    detector_hog, mmod_detector = initialize.initialize_detectors()
    cap = cv2.VideoCapture(1)
    detection_history = deque(maxlen=5) 
    reset_interval = 1
    start_time = time.time()
    buffer_percentage = 0.08

    frame_height, frame_width = cap.read()[1].shape[:2]
    roi_x, roi_y = 0, 0
    roi_w, roi_h = frame_width, frame_height

    prev_time = 0

    root.bind_all("<Key>", handle_key_press)



    video_canvas.focus_set()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        elapsed_time = time.time() - start_time

        roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        detected_Faces = face_detection.detect_faces(roi_frame, detector_hog, mmod_detector)
        detection_history.append(1 if len(detected_Faces) > 0 else 0)
        
        
        for k, d in enumerate(detected_Faces):
            shape = sp(roi_frame, d) 
            roi_frame_rgb = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
            face_descriptor = facerec.compute_face_descriptor(roi_frame_rgb, shape)
            name = identify_face(face_descriptor, saved_embeddings, saved_labels)
            add_to_user_Names_for_oneNote(name)
           
            label_position = (d.left() + roi_x, max(d.top() + roi_y - 10, 15))
            cv2.putText(frame, name, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if sum(detection_history) >= 4 and len(detected_Faces) > 0:
            sorted_faces = sorted(detected_Faces, key=lambda rect: rect.top())  
            first_face = sorted_faces[0]
            last_face = sorted_faces[-1]

            buffer_w = int(buffer_percentage * frame_width)
            buffer_h = int(buffer_percentage * frame_height)

        
            roi_x = max(0, roi_x + first_face.left() - buffer_w)
            roi_y = max(0, roi_y + first_face.top() - buffer_h)
            roi_w = min(frame_width - roi_x, (last_face.right() - first_face.left()) + 2 * buffer_w)
            roi_h = min(frame_height - roi_y, (last_face.bottom() - first_face.top()) + 2 * buffer_h)
    
        if elapsed_time > reset_interval:
            roi_x, roi_y = 0, 0
            roi_w, roi_h = frame_width, frame_height
            start_time = time.time()  

        frame = display.display_results(frame, detected_Faces, roi_x, roi_y, roi_w, roi_h)


        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        fps_counter.update(fps)
        cv2.putText(frame, f"{fps:.2f}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)


        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(image=frame_pil)
        video_canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        video_canvas.image = frame_tk

        video_canvas.update()
        if is_namelist_requested:
            print(user_Names_for_oneNote)
            is_namelist_requested=False
        if user_celar_requested:
            user_Names_for_oneNote.clear()
            print("user list cleared")
            user_celar_requested=False
        if add_person_clicked or exit_requested or all_windows_closed:
            break

    cap.release()
    cv2.destroyAllWindows()
    
    
        

    if add_person_clicked:
        video_canvas.master.destroy()
        open_face_capture_window()
        all_windows_closed = True

    if exit_requested:
        print(user_Names_for_oneNote)
        root.quit() 
