import person_dao_impl
import model
import face


# 更新全局人脸库
def updateGlFaceLib():
    # 获取数据库操作
    p = person_dao_impl.PersonDaoImpl()
    p.updateGlFaceLib()

# 添加人员到数据库流程
def addPerson(image,person):
    # 获取数据库操作
    p = person_dao_impl.PersonDaoImpl()

    # 获取人脸数组
    image_numpy = face.imageFile2Numpy(image)
    # 获取人脸数组
    encode = face.getFaceEncode(image_numpy)

    # 查找人脸是否存在
    if face.findFaceInLib(encode) is True:# 如果存在
        return False
    else:
        person.faceid = encode

    # 人脸图片转码
    person.pic = image_numpy

    # 添加到数据库
    p.addPerson(person)

    # 更新数据库信息到本地
    p.updateGlFaceLib()

    return True




if __name__ == '__main__':

    # # 加载全局人脸库
    # updateGlFaceLib()
    #
    # # 打印全局人脸库
    # print(gl.face_dict)
    #
    # # 添加人脸
    # addPerson("image/拜登1.jpg", model.Person("拜登", 1))
    #
    # # 打印全局人脸库
    # print(gl.face_dict)

    print(addPerson("image/拜登1.jpg", model.Person("拜登", 1)))
