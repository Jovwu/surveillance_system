import json
import time
import ast
import face_recognition


# 将图像转化为Numpy数组
import numpy
from cv2 import cv2

import person_dao_impl
from model import Person
import scipy

from tools import list2Str, str2List

def imageFile2Numpy(imageFile,mode = 'L'):
    return face_recognition.load_image_file(imageFile,mode=mode)


# 获得人脸在图片中的位置
def getFaceLocations(imageArr):
    return face_recognition.face_locations(imageArr)# ,model='cnn'开启GPU加速


# 获得人脸编码
def getFaceEncode(imageArr,known_face_locations = None):
    return face_recognition.face_encodings(imageArr,known_face_locations=known_face_locations)

# 判断人脸是否在人脸库
def isFaceExist(knowList,target):
    return face_recognition.compare_faces(knowList,target)

# 返回人脸ID 若没有则为0
def getFaceOf(target,dict):

    id = 0
    for key,value in dict.items():
        res = isFaceExist([value,],target)[0]
        # 查找人脸
        if res:
            id = key
            break
    return id

# 添加人脸到全局人脸库
def addFaceID(name, image):
    pass


if __name__ == '__main__':

    def openCamera():
        cap = cv2.VideoCapture(2)
        faceEncoding = None
        while (1):
            time.sleep(0.06)
            # get a frame
            ret, frame = cap.read()
            # show a frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faceLocation = getFaceLocations(frame)
            # 获得人脸位置
            if len(faceLocation) == 0:
                print("没有人脸")
                continue
            else:
                # 获得人脸编码 # .repeat(3, 2)
                faceEncoding = getFaceEncode(frame,faceLocation)
                print("人脸编码为：{0}".format(faceEncoding[0]))
                print(type(faceEncoding[0]))
                break


        cap.release()
        cv2.destroyAllWindows()
        return faceEncoding

    PDI = person_dao_impl.PersonDaoImpl()

    # 当前人脸
    enc = openCamera()[0]

    # 添加用户
    #PDI.addPerson(Person(enc, "zsy", 1, "pic"))
    print(PDI.getAllPersonFace())
    print(getFaceOf(enc,PDI.getAllPersonFace()))

    # allList = list(PDI.getAllPersonFace().values())
    # print(allList)

    #newList = list()
    #newList.append(PDI.getLastPersonFace()[22])

    # print(isFaceExist(allList,enc))












    # # 将数组转为字符串
    # str1 = list2Str(enc)
    #
    # # 将字符串转数组
    # list1 = str2List(str1)
    # np = numpy.array(list1)
    # print(np)
    # print(type(np))
    #
    # print((enc==np).all())


    #cl = ast.literal_eval(st)
    #print(cl)
    #PDI.addPerson(Person(st,"zsy",1,"pic"))


    # 将list转为字典
    # D = {}
    # D["s"] = enc.tolist()
    # # 将字典转为JSON
    # J = json.dumps(D)
    # print(J)
    # print(type(J))
    #PDI.addPerson(Person(J, "zsy", 1, "pic"))

    #
