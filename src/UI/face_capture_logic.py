import sys
sys.path.append('C:/Users/abhin/Desktop/face-identification-opencv/src')
import cv2
import time
import os
import threading
from FaceDetection.detectors import face_detection ,initialize,display
from tkinter import simpledialog
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from FaceId.training_data.recogTraining import train_model



def start_face_capture(video_canvas, start_capturing=False):
    #for capture
    cap = cv2.VideoCapture(0)
    captured_images = []
    continue_updating = True  
    detector_hog, mmod_detector = initialize.initialize_detectors()

    def update_canvas():
        ret, frame = cap.read()
        if not ret:
            return
        detected_faces = face_detection.detect_faces(frame, detector_hog, mmod_detector)

        if detected_faces:
            face = detected_faces[0]
            roi_x, roi_y, roi_w, roi_h = face.left(), face.top(), face.width(), face.height()
            frame = display.display_results(frame, detected_faces, roi_x, roi_y, roi_w, roi_h, show_roi=True)
        else:
            roi_x, roi_y, roi_w, roi_h = 0, 0, frame.shape[1], frame.shape[0]

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(image=frame_pil)
        video_canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        video_canvas.image = frame_tk

        if continue_updating:
            video_canvas.after(10, update_canvas)  

    def capture_images():
        nonlocal continue_updating  
        
        start_time = time.time()
        while time.time() - start_time < 3.3:
            ret, frame = cap.read()
            if not ret:
                break
            detected_faces = face_detection.detect_faces(frame, detector_hog, mmod_detector)
            for face in detected_faces:
                x, y, w, h = (face.left(), face.top(), face.width(), face.height())
                cropped_face = frame[y:y+h, x:x+w]
                captured_images.append(cropped_face)

        continue_updating = False  
        cap.release() 

        name = simpledialog.askstring("Input", "What's your name?")
        if name:
            save_path = f"src/FaceId/training_data/Picture_db/{name}"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
                print(f"User: {name} added to databse")
            else:
                print(f"user {name} already exists.")
            for idx, img in enumerate(captured_images):
                cv2.imwrite(os.path.join(save_path, f"{name}_{idx}.jpg"), img)

        video_canvas.master.master.destroy()
        video_canvas.master.master.master.destroy()
        train_model()

    update_canvas() 
    if start_capturing:
        capture_images()

