import time

import cv2
import numpy as np

def openCamera():
    cap = cv2.VideoCapture(0)
    while(1):
        time.sleep(0.06)
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    openCamera()