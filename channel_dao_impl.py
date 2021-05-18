import sql_base


class ChannelDaoImpl:

    def __init__(self):
        self.__conn = sql_base.MySqlConn()

    # 返回所有通道
    def getAllChannel(self):

        sql = "SELECT channel_id,channel_name,addr.addr_name,Device.device_class,Device.device_arg,Mode.mode_name"\
            " FROM Channel,addr,Device,Mode"\
            " WHERE addr.addr_id = Channel.addr_id and Device.device_id = Channel.device_id and Mode.mode_id = Channel.mode_id"

        result = list()
        for row in self.__conn.execute(sql):
            result.append(row)
        return result

    # 返回指定通道的功能列表
    def getFeaturesByChannelID(self,channel_id):

        sql = "SELECT Features.features_name from ChannelFeatures,Features " \
              "where channel_id = {0} and Features.features_id = ChannelFeatures.features_id" \
            .format(channel_id)

        result = list()
        for row in self.__conn.execute(sql):
            result.append(row[0])
        return result

    # 返回通道数
    def getChannelCount(self,arg = None):

        sql = ""
        if arg is None:
            sql = "SELECT COUNT(*) FROM Channel;"
        elif arg == 1:
            sql = "SELECT COUNT(*) FROM Channel where mode_id = 1;"
        elif arg == 2:
            sql = "SELECT COUNT(*) FROM Channel where mode_id = 2;"
        elif arg == 3:
            sql = "SELECT COUNT(*) FROM Channel where mode_id = 3;"
        elif arg == 4:
            sql = "SELECT COUNT(*) FROM Channel where mode_id = 4;"

        for row in self.__conn.execute(sql):
            return int(row[0])

    # 根据类型返回通道-》以列表的形势
    def getAllChannelIDByClass(self,arg = None):

        sql = ""
        if arg is None:
            sql = "SELECT channel_id FROM Channel;"
        elif arg == 1:
            sql = "SELECT channel_id FROM Channel where mode_id = 1;"
        elif arg == 2:
            sql = "SELECT channel_id FROM Channel where mode_id = 2;"
        elif arg == 3:
            sql = "SELECT channel_id FROM Channel where mode_id = 3;"
        elif arg == 4:
            sql = "SELECT channel_id FROM Channel where mode_id = 4;"

        result = list()
        for row in self.__conn.execute(sql):
            for re in row:
                result.append(re)

        return  result

    # 返回通道业务类型
    def getChannelServiceClass(self,arg):

        sql = ""
        if arg is "features":
            sql = "SELECT * FROM features;"
        elif arg == "mode":
            sql = "SELECT * FROM mode;"
        elif arg == "personClass":
            sql = "SELECT * FROM personclass;"

        result = dict()
        for row in self.__conn.execute(sql):
            result[row[0]] = row[1]
        return result

    # 根据类型返回地址
    def getAddrByClass(self,arg):

        sql = ""
        if arg is "dorm":
            sql = "SELECT * FROM addr where addr_class = 'dorm';"
        elif arg == "class":
            sql = "SELECT * FROM addr where addr_class = 'class';"

        result = dict()
        result[0] = "None"
        for row in self.__conn.execute(sql):
            result[row[0]] = row[1]
        return result


if __name__ == '__main__':

    p = ChannelDaoImpl()
    # print(p.getAllChannel()[0][0])
    # print(p.getFeaturesByChannelID(1001))
    # print(p.getChannelCount(2))
    # print(p.getAllChannelIDByClass(2))
    # print(p.getChannelServiceClass("mode"))
    # print(p.getChannelServiceClass("features"))
    print(p.getAddrByClass("dorm"))