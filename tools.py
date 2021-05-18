import base64

# 单例模式
import time

import cv2


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner

# jpg转base64
def JPG2Base64(image):

    with open(image, 'rb') as f:  # 以二进制读取图片
        data = f.read()
        return base64.b64encode(data)  # 得到 byte 编码的数据

# 获取当前时间
def getCurTime():
     now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
     # print(now)
     return now

# 获取当前时间
def getCurDateTime():
     now = time.strftime("%Y%m%d", time.localtime(time.time()))
     # print(now)
     return now

# 列表转str
def list2Str(list):
    return str(list).strip('[]')

# str转列表
def str2List(str):
    colist = str.split(' ')
    orgList = list()
    for i in colist:
        if i == '':
            continue
        else:
            orgList.append(float(i))
    return orgList

# 字典根据value找K
def getKeyByValue (dict, value):
    return [k for k, v in dict.items() if v == value][0]

# RGB存文件
def saveRGB2JPG(rbg_img,file_path):
    # 将文件转码为BGR
    bgr_img = cv2.cvtColor(rbg_img, cv2.COLOR_RGB2BGR)
    file_path_ = "{0}.jpg".format(file_path)
    cv2.imwrite(file_path_, bgr_img)
    return file_path_

# 从文件读取RGB
def readJPG2RGB(file_path):
    # 读取JPG图片 变成RGB
    JPG = cv2.imread(file_path)
    return cv2.cvtColor(JPG, cv2.COLOR_BGR2RGB)


if __name__ == '__main__':

    # print(JPG2Base64("image/拜登1.jpg"))
    print(getCurTime())
    print(getCurDateTime())

    img_ = cv2.imread("image/D.jpg")


    img = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)

    img1 = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)

    file = saveRGB2JPG(img1,"person/{0}_{1}".format(1001,getCurDateTime()))
    RGB = readJPG2RGB(file)
    cv2.imshow('picture', RGB)
    cv2.waitKey(0)