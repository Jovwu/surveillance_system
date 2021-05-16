import sqlite3
import tools


@tools.singleton
class MySqlConn:

    # 初始化
    def __init__(self):
        self.__conn = sqlite3.connect("xmlg.db")

    # 关闭数据库
    def close(self):
        self.__conn.close()

    # 语句执行
    def execute(self,sql):
        return self.__conn.cursor().execute(sql)

    # 事务提交
    def commit(self):
        self.__conn.commit()

if __name__ == '__main__':

    # 获得数据库连接
    conn = MySqlConn()
    # 数据库执行
    for row in conn.execute("select * from person"):
        print(row)
    # 关闭数据库连接
    conn.close()
