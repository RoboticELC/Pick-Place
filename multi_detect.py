import cv2
import numpy as np

yellow = [0, 255, 255] 
red = [0, 0, 255]
blue = [255, 0, 0]
green = [0, 255, 0]

RGB_array = []

for array in [red, yellow, blue, green]:
    RGB_array.append(array)

def get_limits(colors):
    # Make another array that only stores the hue
    Hue_array = []
    for color in RGB_array:
        c = np.uint8([[color]])
        hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
        hue = hsvC[0][0][0]
        Hue_array.append(hue)
 
    for hue in Hue_array:
        if hue == 0: # Red 
            lower_red = np.array([hue + 170, 150, 90], dtype=np.uint8)
            upper_red = np.array([hue + 180, 255, 255], dtype=np.uint8)
        if hue == 30: # Yellow
            lower_yellow = np.array([hue - 10, 100, 100], dtype=np.uint8)
            upper_yellow = np.array([hue + 15, 255, 255], dtype=np.uint8)

        if hue == 120: # Blue
            lower_blue = np.array([hue - 30, 150, 90], dtype=np.uint8)
            upper_blue = np.array([hue + 10, 255, 255], dtype=np.uint8)

        if hue == 60: # Green 
            lower_green = np.array([hue - 10, 100, 70], dtype=np.uint8)
            upper_green = np.array([hue + 15, 255, 255], dtype=np.uint8)

    return lower_red, upper_red, lower_yellow, upper_yellow, lower_blue, upper_blue, lower_green, upper_green

def find_contour(contour_color, key):
    eps = 0.03 # High eps --> less points
    for point in contour_color:
        perimeter = cv2.arcLength(point, True)
        area = cv2.contourArea(point)
        approx = cv2.approxPolyDP(point, eps * perimeter, True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if area > 800:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
            if len(approx) == 4: 
                if key == "R":
                    cv2.putText(frame, "Box", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                elif key == "Y":
                    cv2.putText(frame, "Box", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255))
                elif key == "B":
                    cv2.putText(frame, "Box", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                elif key == "G":
                    cv2.putText(frame, "Box", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
            #else:
                #cv2.putText(frame, "None", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red, upper_red, lower_yellow, upper_yellow, lower_blue, upper_blue, lower_green, upper_green = get_limits(RGB_array)
    
    # Red Mask (Not as good) --> Please re-adjust range
    red_mask = cv2.inRange(hsvImage, lower_red, upper_red)
    red_mask_ = cv2.bitwise_and(frame, frame, mask = red_mask)
    # Find Contour (Red)
    contourR, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Yellow Mask
    yellow_mask = cv2.inRange(hsvImage, lower_yellow, upper_yellow)
    yellow_mask_ = cv2.bitwise_and(frame, frame, mask = yellow_mask)
    # Find Contour (Yellow)
    contourY, _ = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Blue Mask
    blue_mask = cv2.inRange(hsvImage, lower_blue, upper_blue)
    blue_mask_ = cv2.bitwise_and(frame, frame, mask = blue_mask)
    # Find Contour (Blue)
    contourB, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Green Mask
    green_mask = cv2.inRange(hsvImage, lower_green, upper_green)
    green_mask_ = cv2.bitwise_and(frame, frame, mask = green_mask)
    # Find Contour (Green)
    contourG, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    find_contour(contourR, "R")
    find_contour(contourY, "Y")
    find_contour(contourB, "B")
    find_contour(contourG, "G")

    cv2.imshow("frame", frame)

    # To Display Mask
    #cv2.imshow("mask", red_mask_)

    # To shut entire process press 'q' on keyboard
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()