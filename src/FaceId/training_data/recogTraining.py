import dlib
import os
import cv2
import pickle
import ctypes

def train_model():
    ctypes.cdll.LoadLibrary("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/zlibwapi.dll")

    face_rec_model_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/dlib_face_recognition_resnet_model_v1.dat"
    shape_predictor_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/shape_predictor_68_face_landmarks.dat"
    training_data_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/Picture_db"

    print("model training started")


    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(shape_predictor_path)
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)

    embeddings = []
    labels = []

    for person_name in os.listdir(training_data_path):
        person_dir = os.path.join(training_data_path, person_name)
        if os.path.isdir(person_dir): 

            for image_name in os.listdir(person_dir):
                if not (image_name.endswith('.jpg') or image_name.endswith('.png')):
                    continue

                image_path = os.path.join(person_dir, image_name)
                img = cv2.imread(image_path)
                
                if img is None:
                    print(f"Failed to load image at path: {image_path}")
                    continue

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                

                dets = detector(gray, 1)
                for k, d in enumerate(dets):
                    shape = sp(img, d)

                    face_descriptor = facerec.compute_face_descriptor(img, shape)
                    embeddings.append(face_descriptor)
                    labels.append(person_name)

    os.makedirs(os.path.dirname("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data"), exist_ok=True)
    with open("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/embeddings.pkl", "wb") as f:
        pickle.dump((embeddings, labels), f)
    print("model trained")



# for single clcik train


# import dlib
# import os
# import cv2
# import pickle
# import ctypes
# ctypes.cdll.LoadLibrary("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/zlibwapi.dll")

# face_rec_model_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/dlib_face_recognition_resnet_model_v1.dat"
# shape_predictor_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/model/shape_predictor_68_face_landmarks.dat"
# training_data_path = "C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/Picture_db"
# print("model training started. plaease wait")
# # Initialize dlib models
# detector = dlib.get_frontal_face_detector()
# sp = dlib.shape_predictor(shape_predictor_path)
# facerec = dlib.face_recognition_model_v1(face_rec_model_path)

# embeddings = []
# labels = []

# # Iterate through training data
# for person_name in os.listdir(training_data_path):
#     person_dir = os.path.join(training_data_path, person_name)
#     if os.path.isdir(person_dir):  # Check if it's a directory

#             for image_name in os.listdir(person_dir):
#                 if not (image_name.endswith('.jpg') or image_name.endswith('.png')):
#                     continue

#                 image_path = os.path.join(person_dir, image_name)
#                 img = cv2.imread(image_path)
                
#                 if img is None:
#                     print(f"Failed to load image at path: {image_path}")
#                     continue

#                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         # Detect face
#                 dets = detector(gray, 1)
#                 for k, d in enumerate(dets):
#                     shape = sp(img, d)
                    
#                     # Compute embedding
#                     face_descriptor = facerec.compute_face_descriptor(img, shape)
#                     embeddings.append(face_descriptor)
#                     labels.append(person_name)

# # Store embeddings and labels
# os.makedirs(os.path.dirname("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data"), exist_ok=True)
# with open("C:/Users/abhin/Desktop/face-identification-opencv/src/FaceId/training_data/embeddings.pkl", "wb") as f:
#  pickle.dump((embeddings, labels), f)
# print("model trained")
 