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

if os.path.isfile(pngName):
    os.remove(pngName)

ret, frame = cam.read()
cv2.imwrite(pngName, frame)

background = cv2.imread(pngName)
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background, (21, 21), 0)

while True:
    _, frame = cam.read()

    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (21, 21), 0)

    diff = cv2.absdiff(background, g)

    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    resized = cv2.resize(thresh, (10, 10), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    cv2.imshow('resized', resized)

    height, width = resized.shape

    countWhite = 0
    for x in range(0, width):
        for y in range(0, height):
            if resized[x, y] == 255:
                countWhite += 1

    if countWhite >= 30:
        print(1)
    else:
        print(0)

    if cv2.waitKey(1) == ord('x'):
        break

os.remove(pngName)
cam.release()
cv2.destroyAllWindows()
os.remove(pngName)
