import io
import sqlite3

import numpy

import tools


@tools.singleton
class MySqlConn:

    # 初始化
    def __init__(self):
        self.__conn = sqlite3.connect("xmlg.db",check_same_thread=False)

        # Converts np.array to TEXT when inserting
        sqlite3.register_adapter(numpy.ndarray, self.adapt_array)

        # Converts TEXT to np.array when selecting
        sqlite3.register_converter("array", self.convert_array)


    # 关闭数据库
    def close(self):
        self.__conn.close()

    # 语句执行
    def execute(self,sql):
        return self.__conn.cursor().execute(sql)

    # 事务提交
    def commit(self):
        self.__conn.commit()

    def adapt_array(arr):
        """
        http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
        """
        out = io.BytesIO()
        numpy.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        out = io.BytesIO(text)
        out.seek(0)
        return numpy.load(out)



if __name__ == '__main__':

    # 获得数据库连接
    conn = MySqlConn()
    # 数据库执行
    for row in conn.execute("select * from person"):
        print(row)
    # 关闭数据库连接
    conn.close()
