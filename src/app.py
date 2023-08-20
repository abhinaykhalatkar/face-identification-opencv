import tkinter as tk
from FaceDetection import faceDetection_dlib
import ctypes

ctypes.cdll.LoadLibrary("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/zlibwapi.dll")

def main():
    root = tk.Tk()
    root.title("Face Identification")

    # Create a frame for the video feed
    video_frame = tk.Frame(root)
    video_frame.pack(side=tk.LEFT, padx=10, pady=10) 

    video_canvas = tk.Canvas(video_frame, width=640, height=480)
    video_canvas.pack()

    # Create a frame for the button
    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    add_person_btn = tk.Button(btn_frame, text="Add Person=>", command=faceDetection_dlib.on_add_person_click)
    add_person_btn.pack()

    root.after(10, lambda: faceDetection_dlib.run_face_detection(video_canvas, root))
    root.mainloop()