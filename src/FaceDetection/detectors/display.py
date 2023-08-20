import cv2

def display_results(frame, faces_hog, roi_x, roi_y, roi_w, roi_h):
    for rect in faces_hog:
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        cv2.rectangle(frame, (x + roi_x, y + roi_y), (x + w + roi_x, y + h + roi_y), (0, 255, 0), 2)
    
    # Draw the ROI rectangle
    # cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2)
    
    return frame


