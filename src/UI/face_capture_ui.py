import tkinter as tk
from .face_capture_logic import start_face_capture

def open_face_capture_window():
    window = tk.Toplevel()
    window.title("Face Capture")

    message_label = tk.Label(window, text="Once clicked on capture button please turn your face from left to right and right to left over 5 seconds")
    message_label.pack(pady=10)

    video_frame = tk.Frame(window)
    video_frame.pack(side=tk.LEFT, padx=10, pady=10)

    video_canvas = tk.Canvas(video_frame, width=640, height=480)
    video_canvas.pack()

    btn_frame = tk.Frame(window)
    btn_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    capture_btn = tk.Button(btn_frame, text="Capture", command=lambda: start_face_capture(video_canvas, start_capturing=True))
    capture_btn.pack()

    start_face_capture(video_canvas, start_capturing=False)

    window.mainloop()
