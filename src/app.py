import sys
sys.path.append('C:/Users/abhin/Desktop/face-identification-opencv/src')
import tkinter as tk
from FaceDetection import faceDetection_dlib
import ctypes
import os,time,subprocess


ctypes.cdll.LoadLibrary("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/zlibwapi.dll")

def main():
    def is_token_expired():
        try:
            with open('src/cred/token_expiry_time.txt', 'r') as f:
                expiry_time = float(f.read())
                return time.time() > expiry_time
        except:
            return True

    if is_token_expired():
        process = subprocess.Popen(['python', 'src/cred/oneNoteCredentials.py'])
        process.wait()
        # os.system('python src/cred/oneNoteCredentials.py')
        
    root = tk.Tk()
    root.title("Face Identification")

    video_frame = tk.Frame(root)
    video_frame.pack(side=tk.LEFT, padx=10, pady=10) 

    video_canvas = tk.Canvas(video_frame, width=640, height=480)
    video_canvas.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    add_person_btn = tk.Button(btn_frame, text="Add Person=>", command=faceDetection_dlib.on_add_person_click)
    add_person_btn.pack()

    root.after(10, lambda: faceDetection_dlib.run_face_detection(video_canvas, root))
    root.mainloop()