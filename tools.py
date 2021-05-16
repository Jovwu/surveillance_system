import base64

# 单例模式
import time


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
     now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
     # print(now)
     return now



if __name__ == '__main__':

    print(JPG2Base64("image/拜登1.jpg"))
    print(getCurTime())