"""
Install OpenCV
1. Ctrl + Alt + S
2. Go to project -> Python Interpreter -> Click '+' icon (top left)
3. Type 'opencv' and install

How to use camera?
1. Run 'takeSample.py'
2. Position your camera, so it can only see the background
3. Press 'c' on the keyboard
4. Program will end and give you file named 'background.png',
    it is vital for noice detection
5. Run this script
"""

import cv2
import os

# Camera
cam = cv2.VideoCapture(0)

pngName = "background.png"

background = cv2.imread(pngName)
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background, (21, 21), 0)

while True:
    # Read frame
    _, frame = cam.read()

    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (21, 21), 0)

    diff = cv2.absdiff(background, g)

    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    cv2.imshow('frame', frame)
    cv2.imshow('thresh', thresh)
    cv2.imshow('diff', diff)

    if cv2.waitKey(1) == ord('x'):
        break

os.remove(pngName)
cam.release()
cv2.destroyAllWindows()
