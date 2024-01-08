#https://www.geeksforgeeks.org/python-opencv-gettrackbarpos-function/
import cv2
import numpy as np

def nothing(x):
    pass

# Trackbar
cv2.namedWindow("frame")
cv2.createTrackbar("H", "frame", 0, 180, nothing)
cv2.createTrackbar("S", "frame", 255, 255, nothing)
cv2.createTrackbar("V", "frame", 255, 255, nothing)

# x = 500 (width), y = 250 (height), z = 3 --> HSV
img_hsv = np.zeros((250, 500, 3), np.uint8)

while True:
    h = cv2.getTrackbarPos("H", "frame")
    s = cv2.getTrackbarPos("S", "frame")
    v = cv2.getTrackbarPos("V", "frame")

    img_hsv[:] = (h, s, v)
    img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    # All first row, first depth
    Blue = img_bgr[0][0][0]
    Green = img_bgr[1][0][1]
    Red = img_bgr[2][0][2]

    #img_bgr = cv2.rectangle(img_bgr, (0, 0), (250, 250), (0, 0, 0), -1)
    #cv2.putText(img_bgr,"RGB",(100,100),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (Red, Green, Blue),1,cv2.LINE_AA)
    
    print("R: ", Red, " G: ", Green, " B: ", Blue)
    cv2.imshow("frame", img_bgr)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()