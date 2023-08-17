def get_roi(frame, roi_x_percent, roi_y_percent, roi_w_percent, roi_h_percent):
    frame_height, frame_width = frame.shape[:2]
    roi_x = int(frame_width * roi_x_percent)
    roi_y = int(frame_height * roi_y_percent)
    roi_w = int(frame_width * roi_w_percent)
    roi_h = int(frame_height * roi_h_percent)
    roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    return roi_frame, roi_x, roi_y, roi_w, roi_h
