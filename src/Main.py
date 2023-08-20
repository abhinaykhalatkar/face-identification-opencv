import tkinter as tk
from FaceDetection import faceDetection_dlib
import hupper
import app  # Import the module you just created

if __name__ == "__main__":
    reloader = hupper.start_reloader('app.main')  # Note the 'app.main' here
    app.main()