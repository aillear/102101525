from Support.Delegate import Delegate


class EventCenter:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__event_dic = {}

    def AddEventListener(self, name: str, action):
        if name in self.__event_dic:
            self.__event_dic[name] += action
        else:
            self.__event_dic[name] = Delegate(action)

    def RemoveEventListener(self, name: str, action):
        if name in self.__event_dic:
            self.__event_dic[name] -= action

    def EventTrigger(self, name: str, *args, **kwargs):
        if name in self.__event_dic:
            self.__event_dic[name](*args, **kwargs)

    def DeleteEvent(self, name: str):
        if name in self.__event_dic:
            del self.__event_dic[name]

    def Clear(self):
        self.__event_dic = {}