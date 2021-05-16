def login(loginInfo):
    # 判断登陆方式
    if loginInfo['mode'] == "info":
        # 用户名密码登录
        result = selectUserByIDAndPwd(loginInfo['id'], loginInfo['pwd'])
    else:
        # 人脸登录
        result = selectUserByFaceID(loginInfo['faceid'])
    # 返回结果
    return result


def selectUserByIDAndPwd(id,pwd):
    return bool

def selectUserByFaceID(faceid):
    return bool