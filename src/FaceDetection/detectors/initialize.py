import dlib
import os

def initialize_detectors():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "..", "pre-trained-model", "mmod_human_face_detector.dat")
    detector_hog = dlib.get_frontal_face_detector()
    mmod_detector = dlib.cnn_face_detection_model_v1(model_path)
    return detector_hog, mmod_detector
