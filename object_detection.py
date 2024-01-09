import cv2
import numpy as np

yellow = [0, 255, 255] 
red = [0, 0, 255]
blue = [255, 0, 0]
green = [0, 255, 0]

def get_hsv(color): 
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV) 
    hue = hsvC[0][0][0]  # Get the hue value 
    if hue == 30: # Yellow
        lower_limit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_limit = np.array([hue + 15, 255, 255], dtype=np.uint8)
    if hue == 60: # Green 
        lower_limit = np.array([hue - 10, 100, 70], dtype=np.uint8)
        upper_limit = np.array([hue + 15, 255, 255], dtype=np.uint8)
    if hue == 120: # Blue
        lower_limit = np.array([hue - 30, 150, 90], dtype=np.uint8)
        upper_limit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    if hue == 0: # Red 
        lower_limit = np.array([hue + 170, 150, 90], dtype=np.uint8)
        upper_limit = np.array([hue + 180, 255, 255], dtype=np.uint8)

    return lower_limit, upper_limit

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_limit, upper_limit = get_hsv(color = blue)

    # Make Color Mask 
    mask = cv2.inRange(hsvImage, lower_limit, upper_limit)
    color_mask = cv2.bitwise_and(frame, frame, mask = mask)

    # Find Contour (1 Color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Detect Shape(s)
    for point in contours:
        area = cv2.contourArea(point)
        approx = cv2.approxPolyDP(point, 0.02*cv2.arcLength(point, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
            if len(approx) == 4:
                cv2.putText(frame, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
            else:
                cv2.putText(frame, "Un-Identified", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

    cv2.imshow("frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("colored mask",color_mask)

    # To shut entire process press 'q' on keyboard
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()