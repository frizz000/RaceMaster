import cv2
import os

# Camera
cam = cv2.VideoCapture(0)

pngName = "background.png"

if os.path.isfile(pngName):
    os.remove(pngName)

while True:
    # Read frame
    ret, frame = cam.read()

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('c'):
        ret, back = cam.read()
        cv2.imwrite(pngName, frame)
        break

cam.release()
cv2.destroyAllWindows()
