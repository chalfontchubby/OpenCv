# import the opencv library
import cv2
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)
green = np.uint8([[[0,255,0 ]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print( hsv_green )
while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.asarray([40,50,50])  # white!
    upper_green = np.asarray([80, 255, 255])  # yellow! note the order
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(img_hsv, lower_green, upper_green)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0 :
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if  M['m00'] > 0 :
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            print(f"{cx} {cy}")
            cv2.drawContours(res, c, -1, (0, 0, 255), 3)
    cv2.imshow("mask", mask)  # this colormap will display in black / white
    cv2.imshow("res", res)  # this colormap will display in black / white
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows() 