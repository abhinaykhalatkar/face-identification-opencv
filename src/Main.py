import hupper
from FaceDetection import faceDetection_dlib

def main():
    reloader = hupper.start_reloader('Main.main')
    faceDetection_dlib.run_face_detection()

if __name__ == "__main__":
    main()
    