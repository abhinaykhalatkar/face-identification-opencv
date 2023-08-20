import tkinter as tk
from FaceDetection import faceDetection_dlib
import hupper
import app  

if __name__ == "__main__":
    reloader = hupper.start_reloader('app.main')
    app.main()
    
