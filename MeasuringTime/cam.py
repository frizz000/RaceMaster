"""
Class takes care of measuring runners time.
"""

import cv2
import os
import time


class Camera:
    def __init__(self, sensitivity):
        self.pngName = "../background.png"
        self.sensitivity = sensitivity
        self.camera = cv2.VideoCapture(0)

    def captureBackground(self):
        """
        Method simply takes a frame from camera and save it as .png file
        """
        ret, frame = self.camera.read()
        cv2.imwrite(self.pngName, frame)

    @staticmethod
    def formatFrame(frame):
        """
        Method format given frame to the shades of gray

        :param frame: Frame we want to format
        :return: Formatted frame
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        return frame

    def readTime(self):
        """
        Core function of this class. Method takes a frame compares it with background. If movement is detected method
        measure time and returns it when user preses 'q' to quit.
        :return: Measured time from first detected movement
            to the second detected movement min. 3 seconds after the first one.
        """
        startTime = None
        runTime = None

        background = cv2.imread(self.pngName)
        background = self.formatFrame(background)

        while True:
            _, frame = self.camera.read()

            frame = self.formatFrame(frame)

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

            if countWhite > (height * width) * (self.sensitivity / 100):
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

    def start(self):
        """
        Method that starts process of time measurement.

        :return: Measured time
        """
        if os.path.isfile(self.pngName):
            os.remove(self.pngName)

        self.captureBackground()
        runTime = self.readTime()

        os.remove(self.pngName)
        self.camera.release()
        cv2.destroyAllWindows()

        runTime = round(runTime, 3)
        return runTime