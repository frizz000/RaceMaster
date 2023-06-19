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
import time


def captureBackground(pngName, cam):
    ret, frame = cam.read()
    cv2.imwrite(pngName, frame)


def formatFrame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    return frame


def readTime(pngName, cam, sensitivity):
    startTime = None
    finishTime = None
    runTime = None

    background = cv2.imread(pngName)
    background = formatFrame(background)

    while True:
        _, frame = cam.read()

        frame = formatFrame(frame)

        diff = cv2.absdiff(background, frame)
        thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        resized = cv2.resize(thresh, (25, 25), fx=0, fy=0, interpolation=cv2.THRESH_BINARY)

        cv2.imshow('resized', resized)

        height, width = resized.shape

        countWhite = 0
        for x in range(0, width):
            for y in range(0, height):
                if resized[x, y] > 0:
                    countWhite += 1

        if countWhite > (height * width) * (sensitivity / 100):
            if startTime is None:
                startTime = time.time()
                print("-=- Started measuring time -=-")

            finishTime = time.time()
            tempTime = finishTime - startTime

            if tempTime > 3:
                if runTime is None:
                    runTime = tempTime
                    print("-=- Finished measuring time -=-")

        if cv2.waitKey(1) == ord('q'):
            if runTime is None:
                runTime = 0

            return runTime


def startCam():
    cam = cv2.VideoCapture(0)
    pngName = "../background.png"
    sensitivity = 30

    if os.path.isfile(pngName):
        os.remove(pngName)

    captureBackground(pngName, cam)
    runTime = readTime(pngName, cam, sensitivity)

    os.remove(pngName)
    cam.release()
    cv2.destroyAllWindows()

    runTime = round(runTime, 3)
    return runTime


print(startCam())
