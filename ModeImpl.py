class Mode:

    def __init__(self):
        self.features = []
        self.channel = None

    # 设置通道
    def setChannel(self, channel):

        self.channel = channel
        # 给功能设置通道
        for fob in self.features:
            fob.setChannel(channel)

    # 模式运行
    def run(self):
        pass
        # 此处用于与人脸库进行比对
        # 将结果写入数据库（使用数据库线程池）

    # 添加功能
    def addFeatures(self,features):
        self.features.append(features)

    # 删除功能
    def deleteFeatures(self,features):
        pass


class Monitor(Mode):

    def __init__(self):
        super().__init__()
        pass

    def run(self):
        return {"position":0,"text":None}

class ClassMode(Mode):

    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


class DormIn(Mode):

    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


class DormOut(Mode):

    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass
