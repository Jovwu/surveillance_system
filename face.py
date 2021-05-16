import time

import face_recognition


# 将图像转化为Numpy数组
def imageFile2Numpy(imageFile):
    return face_recognition.load_image_file(imageFile)


# 获得人脸在图片中的位置
def getFaceLocations(imageArr):
    return face_recognition.face_locations(imageArr)# ,model='cnn'开启GPU加速


# 获得人脸编码
def getFaceEncode(imageArr):
    return face_recognition.face_encodings(imageArr)[0]


# 判断人脸是否存在于全局人脸库
# def findFaceInLib(image_encoding):
#     for id in gl.face_dict:
#
#         results = face_recognition.compare_faces([gl.face_dict[id]], image_encoding)
#
#         if results[0]:
#             return True
#     else:
#         return False


# 添加人脸到全局人脸库
def addFaceID(name, image):
    pass


if __name__ == '__main__':

    print(getFaceLocations(imageFile2Numpy("image/拜登1.jpg")))



    #
