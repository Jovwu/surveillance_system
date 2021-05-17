import traceback

import cv2
import numpy

import sql_base as sql_base
import model as model
import sqlite3


class PersonDaoImpl:

    def __init__(self):
        self.__conn = sql_base.MySqlConn()

    # 返回所有人员
    def getAllPerson(self):

        sql = "SELECT * FROM person"

        result = list()
        for row in self.__conn.execute(sql):
            result.append(row)
        return result

    # 添加人员
    def addPerson(self,person):


        sql = "INSERT INTO person ({0[1]},{0[2]},{0[3]},{0[4]}) VALUES ('{1}', '{2}', {3}, '{4}')"\
            .format(model.person_col, person.faceid, person.name, person.class_id, person.pic)




        try:
            self.__conn.execute(sql)
            self.__conn.commit()
        except Exception as e:
            traceback.print_exc()
            return False

        return True

    # 删除指定人员
    def deletePerson(self, id):

        sql = "DELETE from person where {0[0]} = {1}" \
            .format(model.person_col, id)

        try:
            self.__conn.execute(sql)
            self.__conn.commit()
        except Exception as e:
            traceback.print_exc()
            return False

        return True

    # 加载全局人脸库
    def getAllPersonFace(self):

        sql = "SELECT person_id,person_faceid FROM person"

        result = dict()
        for row in self.__conn.execute(sql):
            result[row[0]] = numpy.fromstring(row[1][1:-2], dtype=float, sep=' ')
        return result

    # 加载最后一条记录
    def getLastPersonFace(self):

        sql = "SELECT * FROM person ORDER BY person_id DESC LIMIT 1;"

        result = dict()
        for row in self.__conn.execute(sql):
            result[row[0]] = numpy.fromstring(row[1][1:-2], dtype=float, sep=' ')
        return result

    # 根据姓名查找指定人员（模糊搜索）

    # 查找指定人员

    # 返回所有人脸ID->用字典对应{"id":"faceid"}
    # def updateGlFaceLib(self):
    #
    #     # 先判断是更新最新记录还是全部记录
    #     if gl.face_dict_flag == 0:
    #
    #         sql = "SELECT {0[0]},{0[1]} FROM person".format(model.person_col)
    #
    #         result = dict()
    #         for row in self.__conn.execute(sql):
    #             result[row[0]] = row[1]
    #
    #         gl.face_dict = result
    #         gl.face_dict_flag = 1
    #
    #     else:
    #
    #         sql = "SELECT * FROM person WHERE {0[0]} = (SELECT MAX({0[0]}) FROM Person)".format(model.person_col)
    #
    #         for row in self.__conn.execute(sql):
    #             gl.face_dict[row[0]] = row[1]




    # 根据ID返回姓名



if __name__ == '__main__':

    p = PersonDaoImpl()

    print(p.getAllPersonFace())
    print(p.getLastPersonFace())
    # # geyAllPerson测试
    # print(p.getAllPerson())

    # # addPerson测试
    # print(p.addPerson(person=model.Person("1", "1", 1, "1")))

    # # deletePerson测试
    # print(p.deletePerson(1))

    # # updateGlFaceLib测试
    # p.updateGlFaceLib()
    # print(gl.face_dict)


    # 关闭数据库

