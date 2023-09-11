class DataKeeper:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.info_dic = {}

    def SendData(self, name: str,  data):
        self.info_dic[name] = data

    def GetData(self, name: str):
        # 反正None就返回None了呗
        return self.info_dic.get(name)
