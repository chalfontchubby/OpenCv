# import the opencv library
import cv2
import numpy as np
from picamera2 import Picamera2
import time
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888"}))
picam2.start()

title_red_min = 'Lower hue threshold'
title_red_max = 'Upper hue threshold'
title_val_min = 'Lower val'
title_sat_min = 'Lower sat'
title_erode = 'Erode'

erosion_size = 0
max_elem = 2
max_kernel_size = 21
title_mask_window = 'Mask Calibration'

def mask_func(frame, img_hsv, value):
    min_red = cv2.getTrackbarPos(title_red_min, title_mask_window)
    max_red = cv2.getTrackbarPos(title_red_max, title_mask_window)
    min_val = cv2.getTrackbarPos(title_val_min, title_mask_window)
    min_sat = cv2.getTrackbarPos(title_sat_min, title_mask_window)
    erosion = cv2.getTrackbarPos(title_erode, title_mask_window)

    lower_red = np.asarray([min_red,min_sat,min_val])  # white!
    upper_red = np.asarray([max_red, 255, 255])  # yellow! note the order
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(img_hsv, lower_red, upper_red)

    #kernel = np.ones((erosion, erosion), np.uint8)
    #eroded = cv2.erode(mask, kernel)
    #dilated = cv2.dilate(eroded, kernel)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame, frame, mask=dilated)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0 :
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if  M['m00'] > 0 :
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            print(f"{cx} {cy}")
            #
            cv2.drawContours(frame, c, -1, (0, 0, 255), 3)
    #cv2.imshow("mask", mask)  # this colormap will display in black / white
    #cv2.imshow("dilated", dilated)  # this colormap will display in black / white
    cv2.imshow("res", frame)  # this colormap will display in black / white


cv2.namedWindow(title_mask_window)
cv2.createTrackbar(title_red_min, title_mask_window, 10, 255, mask_func)
cv2.createTrackbar(title_red_max, title_mask_window, 52, 255, mask_func)
cv2.createTrackbar(title_val_min, title_mask_window, 10, 255, mask_func)
cv2.createTrackbar(title_sat_min, title_mask_window, 180, 255, mask_func)
cv2.createTrackbar(title_erode, title_mask_window, 4, 20, mask_func)

# define a video capture object
vid = cv2.VideoCapture(0)
green = np.uint8([[[0,255,0 ]]])
red = np.uint8([[[0,0,255]]])

while (True):
    ret, frame = vid.read()
    picam2.start()
    frame = picam2.capture_array()
    picam2.stop()

    resized = cv2.resize(frame, (256, 200))
    # Display the resulting frame
    #cv2.imshow('frame', resized)
    cropped = resized[32:224,32:168]
    img_hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    mask_func(cropped, img_hsv,0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()