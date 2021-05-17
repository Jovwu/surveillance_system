import time

import cv2
import numpy as np

from face import getFaceLocations


def openCamera():
    cap = cv2.VideoCapture(2)
    faceLocation = None
    while(1):
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
        # get a frame
        ret, frame = cap.read()
        # 转码
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faceLocation = getFaceLocations(img)
        print(faceLocation)
        # show a frame
        if len(faceLocation) == 0:
            cv2.imshow("show", frame)
            continue
        else:
            # 遍历人脸位置信息
            for top, right, bottom, left in faceLocation:
                # 对人脸画框
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.imshow("show", frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    openCamera()