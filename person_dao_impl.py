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
    def addPerson(self, person):

        sql = "INSERT INTO person ({0[1]},{0[2]},{0[3]},{0[4]}) VALUES ('{1}', '{2}', {3}, '{4}')" \
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

    # 返回最后一个人员的ID
    def getLastPersonID(self):

        sql = "SELECT person_id FROM person ORDER BY person_id DESC LIMIT 1;"

        result = None
        for row in self.__conn.execute(sql):
            result = row[0]
        return result

    # 设置人员图片所在位置
    def setPersonPicPath(self, person_id, person_pic):

        sql = "UPDATE person SET person_pic = '{0}' where person_id = {1};".format(person_pic, person_id)

        try:
            self.__conn.execute(sql)
            self.__conn.commit()
        except Exception as e:
            traceback.print_exc()
            return False

        return True

    # 获得人员信息
    def getPersonForTable(self, arg=None):
        # 如果arg为None，则表示加载所有
        sql = "SELECT Person.person_id,Person.person_pic,Person.person_name,person.person_class_id," \
              "IFNULL(DormPerson.addr_id,0) AS dorm,IFNULL(GradePerson.addr_id,0) AS grade " \
              "FROM Person " \
              "LEFT JOIN DormPerson on Person.person_id = DormPerson.person_id " \
              "LEFT JOIN GradePerson on Person.person_id = GradePerson.person_id," \
              "PersonClass " \
              "WHERE Person.person_class_id = PersonClass.person_class_id" \

        if arg is None:
            pass
        else:
            sql = sql + " and Person.person_id = {0}".format(arg)

        result = list()
        for row in self.__conn.execute(sql):
            result.append(row)
        return result

    # 修改人员信息
    def updatePerson(self,person,dorm,grade):
        print("开始执行")
        # dormperson表
        # 如果是0
        dic = dict()
        dic["dormperson"] = dorm
        dic["gradeperson"] = grade
        for table,col_value in dic.items():
            isExist = False
            if self.findPersonIDInTable(table, person.id) == 1:  # 有记录
                isExist = True

            if dorm == 0:# 如果设置为none
                if isExist:
                    print("1")
                    self.deletePersonIDInTable(table, person.id)  # 删除记录
            else:# 如果设置为实际值
                if isExist:# 如果存在  更新表
                    print("2")
                    self.updatePersonIDInTable(table,col_value,person.id)
                else:# 不存在 创建记录
                    print("3")
                    self.insertPersonIDInTable(table,col_value,person.id)

        # 判断是否有图片
        if person.pic is None:# 如果没有图
            sql = "UPDATE person SET person_name = '{0}' ," \
                  "person_class_id = {1} " \
                  "where person_id = {2};".format(person.name, person.class_id,person.id)
            # 执行
            try:
                self.__conn.execute(sql)
                self.__conn.commit()
            except Exception as e:
                traceback.print_exc()
                return False
        else:
            return self.updatePerson(person)

        return True

    # 更新用户
    def updatePerson(self,person):

        sql = "UPDATE person SET person_faceid = {0}," \
              "person_name = {1}," \
              "person_class_id = {2}," \
              "person_pic = {3}" \
              " where person_id = {4};" \
              .format(person.faceid, person.name,person.class_id,person.pic,person.id)

        try:
            self.__conn.execute(sql)
            self.__conn.commit()
        except Exception as e:
            traceback.print_exc()
            return False

        return True

    # 查询某张表中 指定person_id是否有记录
    def findPersonIDInTable(self,tabel,person_id):

        sql = "SELECT count(*) FROM {0} where person_id = {1};".format(tabel,person_id)

        result = None
        for row in self.__conn.execute(sql):
            result = row[0]
        return result

    # 删除某张表中的 指定person_id的记录
    def deletePersonIDInTable(self,tabel,person_id):
        sql = "DELETE FROM {0} WHERE person_id = {1};".format(tabel,person_id)

        try:
            self.__conn.execute(sql)
            self.__conn.commit()
        except Exception as e:
            traceback.print_exc()
            return False

        return True

    # 给表添加记录
    def insertPersonIDInTable(self,tabel,col_value,person_id):
        sql = "INSERT INTO {0} values ({1},{2})".format(tabel,col_value,person_id)
        try:
            self.__conn.execute(sql)
            self.__conn.commit()
        except Exception as e:
            traceback.print_exc()
            return False

        return True

    # 给表更新记录
    def updatePersonIDInTable(self,tabel,col_value,person_id):
        sql = "UPDATE {0} SET addr_id = {1} where person_id = {2};".format(tabel, col_value,person_id)
        try:
            self.__conn.execute(sql)
            self.__conn.commit()
        except Exception as e:
            traceback.print_exc()
            return False

        return True

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

    # print(p.getAllPersonFace())
    # print(p.getLastPersonFace())

    #print(p.deletePersonIDInTable("dormperson",51))
    print(p.findPersonIDInTable("dormperson", 51))
    print(p.updatePersonIDInTable("dormperson",3,51))
    print(p.findPersonIDInTable("dormperson", 51))
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
