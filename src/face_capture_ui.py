import tkinter as tk
from tkinter import messagebox
import cv2
import os

root = tk.Tk()
root.title("Face Capture UI")

start_btn = tk.Button(root, text="Start Face Capture", command=start_face_capture)
start_btn.pack(pady=20)