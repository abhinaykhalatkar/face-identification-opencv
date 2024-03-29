# from cred.oneNoteCredentials import access_token
import requests
import webbrowser
import datetime
from UI.face_capture_ui import open_face_capture_window
import tkinter as tk
from PIL import Image, ImageTk
from f1_score_reading import F1ScoreCounter
from fps_reading import FPSCounter
from .detectors import initialize, face_detection, display
from collections import deque
import numpy as np
import dlib
import pickle
import time
import cv2
import sys
sys.path.append('C:/Users/abhin/Desktop/face-identification-opencv/src')
# from UI.face_capture_ui import open_face_capture_window
# from cred.oneNoteCredentials import onenote_instance
def get_access_token_from_file():
    try:
        with open("src/cred/token.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

with open("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/embeddings.pkl", "rb") as f:
    saved_embeddings, saved_labels = pickle.load(f)

face_rec_model_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/dlib_face_recognition_resnet_model_v1.dat"
shape_predictor_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/shape_predictor_68_face_landmarks.dat"
sp = None
facerec = None
all_windows_closed = False
add_person_clicked = False
exit_requested = False
user_Names_for_oneNote = []
is_namelist_requested = False
user_clear_requested = False
should_open_onenote = False
# onenote_instance.get_structure()



def add_to_user_Names_for_oneNote(new_string):
    if new_string not in user_Names_for_oneNote and 'unknown' not in new_string.lower():
        user_Names_for_oneNote.append(new_string)


def initialize_dlib_models():
    global sp, facerec
    sp = dlib.shape_predictor(shape_predictor_path)
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
# 0.40


def identify_face(face_descriptor, saved_embeddings, saved_labels, threshold=0.50):
    distances = [np.linalg.norm(np.array(
        face_descriptor) - np.array(embedding)) for embedding in saved_embeddings]
    min_distance_index = np.argmin(distances)
    if distances[min_distance_index] < threshold:
        return saved_labels[min_distance_index]
    else:
        return "Unknown"


def on_add_person_click():
    global add_person_clicked
    add_person_clicked = True
    
def on_open_oneNote_click():
    global should_open_onenote
    should_open_onenote = True
    
def handle_key_press(event):
    global is_namelist_requested
    global exit_requested
    global user_clear_requested
    if event.char == 'q':
        exit_requested = True
    elif event.char == 'w':
        is_namelist_requested = True
    elif event.char == 'c':
        user_clear_requested = True



def run_face_detection(video_canvas, root):
    global all_windows_closed
    global is_namelist_requested
    global user_clear_requested
    global should_open_onenote
    initialize_dlib_models()
    fps_counter = FPSCounter()
    f1_score_counter = F1ScoreCounter()
    detector_hog, mmod_detector = initialize.initialize_detectors()
    #for capture
    cap = cv2.VideoCapture(0)
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
        detected_Faces = face_detection.detect_faces(
            roi_frame, detector_hog, mmod_detector)
        detection_history.append(1 if len(detected_Faces) > 0 else 0)

        for k, d in enumerate(detected_Faces):
            shape = sp(roi_frame, d)
            roi_frame_rgb = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
            face_descriptor = facerec.compute_face_descriptor(
                roi_frame_rgb, shape)
            name = identify_face(
                face_descriptor, saved_embeddings, saved_labels)
            is_face_detected = len(detected_Faces) > 0
            is_face_present = name != "Unknown"
            f1_score_counter.update(is_face_detected, is_face_present)
            
            add_to_user_Names_for_oneNote(name)

            label_position = (d.left() + roi_x, max(d.top() + roi_y - 10, 15))
            cv2.putText(frame, name, label_position,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if sum(detection_history) >= 4 and len(detected_Faces) > 0:
            sorted_faces = sorted(detected_Faces, key=lambda rect: rect.top())
            first_face = sorted_faces[0]
            last_face = sorted_faces[-1]

            buffer_w = int(buffer_percentage * frame_width)
            buffer_h = int(buffer_percentage * frame_height)

            roi_x = max(0, roi_x + first_face.left() - buffer_w)
            roi_y = max(0, roi_y + first_face.top() - buffer_h)
            roi_w = min(frame_width - roi_x, (last_face.right() -
                        first_face.left()) + 2 * buffer_w)
            roi_h = min(frame_height - roi_y,
                        (last_face.bottom() - first_face.top()) + 2 * buffer_h)

        if elapsed_time > reset_interval:
            roi_x, roi_y = 0, 0
            roi_w, roi_h = frame_width, frame_height
            start_time = time.time()

        frame = display.display_results(
            frame, detected_Faces, roi_x, roi_y, roi_w, roi_h, show_roi=True)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        fps_counter.update(fps)
        current_f1_score = f1_score_counter.calculate_f1_score()
        # cv2.putText(frame, f"{fps:.2f}", (5, 20),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"{user_Names_for_oneNote}", (5, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        #cv2.putText(frame, f"F1-Score: {current_f1_score:.2f}", (5, 40),
        #        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(image=frame_pil)
        video_canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        video_canvas.image = frame_tk

        video_canvas.update()
        if is_namelist_requested:
            print(user_Names_for_oneNote)
            is_namelist_requested = False
        if user_clear_requested:
            user_Names_for_oneNote.clear()
            print("user list cleared")
            user_clear_requested = False
        if should_open_onenote:
            access_token = get_access_token_from_file()

            headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json',
                        'Cache-Control': 'no-cache'
                    }
            print("opening one note...")
            notebooks_url = 'https://graph.microsoft.com/v1.0/me/onenote/notebooks'
            response = requests.get(notebooks_url, headers=headers)
            if response.status_code != 200:
                    print(f"Failed to retrieve notebooks. Status code: {response.status_code}, Response: {response.text}")
                    return
            notebooks = response.json().get('value', [])
            
            # Find the 'student_data' notebook
            student_data_notebook = next(
                (nb for nb in notebooks if nb['displayName'] == 'student_data'), None)
            if student_data_notebook:
                sections_url = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{student_data_notebook['id']}/sections"
                response = requests.get(sections_url, headers=headers)
                if response.status_code != 200:
                    print(f"Failed to retrieve sections. Status code: {response.status_code}, Response: {response.text}")
                    return
                sections = response.json().get('value', [])
                for student_name in user_Names_for_oneNote:
                    # Check if section with student's name exists
                    student_section = next((sec for sec in sections if sec['displayName'].strip().lower() == student_name.strip().lower()), None)
                    
                    # If the section exists, open the first page in it
                    if student_section:
                        pages_url = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{student_section['id']}/pages"
                        response = requests.get(pages_url, headers=headers)
                        pages = response.json().get('value', [])
                        if pages:
                            first_page = pages[0]
                            if 'links' in first_page and 'oneNoteWebUrl' in first_page['links'] and 'href' in first_page['links']['oneNoteWebUrl']:
                                oneNoteWebUrl = first_page['links']['oneNoteWebUrl']['href']
                                webbrowser.open(oneNoteWebUrl, new=2)
                            else:
                                print("Failed to retrieve OneNote web URL.")
                    
                    # If the section doesn't exist, create it and an empty page within
                    else:
                        data = {
                            "displayName": student_name
                        }
                        response = requests.post(sections_url, headers=headers, json=data)
                        
                        if response.status_code == 201:
                            print(f"Section for {student_name} created successfully!")
                            new_section_data = response.json()
                            new_section_id = new_section_data['id']

                            pages_url = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{new_section_id}/pages"
                            boundary = "A300x"
                            current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            headers_multipart = {
                                'Authorization': f'Bearer {access_token}',
                                'Content-Type': f'multipart/form-data; boundary={boundary}',
                                'Cache-Control': 'no-cache'
                            }

                            content = f"--{boundary}\r\n"
                            content += "Content-Disposition: form-data; name=\"Presentation\"\r\n"
                            content += "Content-Type: text/html\r\n\r\n"
                            content += f"""<!DOCTYPE html>
                            <html>
                            <head>
                                <title>{student_name}</title>
                                <meta name={student_name} content="{current_datetime}" />
                            </head>
                            <body>
                                <p>This is an empty page for {student_name}.</p>
                            </body>
                            </html>\r\n"""
                            content += f"--{boundary}--\r\n"

                            response = requests.post(pages_url, headers=headers_multipart, data=content.encode('utf-8'))

                            if response.status_code == 201:
                                new_page_data = response.json()
                                if 'links' in new_page_data and 'oneNoteWebUrl' in new_page_data['links'] and 'href' in new_page_data['links']['oneNoteWebUrl']:
                                    oneNoteWebUrl = new_page_data['links']['oneNoteWebUrl']['href']
                                    webbrowser.open(oneNoteWebUrl, new=2)
                                else:
                                    print("Failed to retrieve OneNote web URL for the newly created page.")
                            else:
                                print(f"Failed to create page in the new section for {student_name}.")
                                print(f"Status Code: {response.status_code}")
                                print(f"Response: {response.text}")
                        else:
                            print(f"Failed to create section for {student_name}.")
                            print(f"Status Code: {response.status_code}")
                            print(f"Response: {response.text}")

            should_open_onenote = False

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
