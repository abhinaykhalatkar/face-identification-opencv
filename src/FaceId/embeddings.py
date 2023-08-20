import tensorflow as tf
import cv2
import numpy as np

class FaceNetEmbeddings:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.input_image_size = (160, 160)

    def preprocess_image(self, face_img):

        face_img = cv2.resize(face_img, self.input_image_size)

        face_img = face_img / 255.0

        face_img = np.expand_dims(face_img, axis=0)
        return face_img

    def get_embedding(self, face_img):
        preprocessed_img = self.preprocess_image(face_img)
        return self.model.predict(preprocessed_img)

if __name__ == "__main__":
    faceNet = FaceNetEmbeddings("C://Users/abhin/Desktop/face-identification-opencv/src/model/facenet/20180402-114759.pb")

