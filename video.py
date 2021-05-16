import time

import numpy as np
import cv2
cap = cv2.VideoCapture('video/testVideo.mp4')

while(cap.isOpened()):

    ret, frame = cap.read()
    #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    time.sleep(0.02)
    if ret:
        cv2.imshow("Image", frame)
    else:
       print('no video')
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
