# import cv2
# def detect_faces(roi, detector_hog, mmod_detector):
#     confidence_threshold = 0.2 
#     gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#     faces_hog = detector_hog(gray_roi)
#     if len(faces_hog) == 0:
#         faces_mmod = mmod_detector(gray_roi, 0)
#         faces_hog = [d.rect for d in faces_mmod if d.confidence > confidence_threshold]
#     return faces_hog


import cv2

def detect_faces(roi, detector_hog, mmod_detector):
    confidence_threshold = 0.2

    # Check if the ROI is empty
    if roi is None or roi.size == 0:
        return []

    try:
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        print(f"Error converting color: {e}")
        return []

    faces_hog = detector_hog(gray_roi)
    if len(faces_hog) == 0:
        faces_mmod = mmod_detector(gray_roi, 0)
        faces_hog = [d.rect for d in faces_mmod if d.confidence > confidence_threshold]
    return faces_hog
