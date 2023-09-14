class Delegate:
    """
    委托
    属性
    """
    def __init__(self, *args):  # 将可调用对象保存为属性, 藏起来
        """
        创建委托, 确保输入的变量都是函数应用,并且参数都一样.返回值无所谓
        传入的变量不可调用报错
        参数数量不一样就报错
        """
        self.__func_list = []
        self.param_num = -1
        # 确保不传入参数的时候不会有问题
        if len(args) == 0:
            return
        func = args[0]
        if callable(func):
            self.param_num = func.__code__.co_argcount
        else:
            raise TypeError('Argument must be callable.')

        for func in args:
            if not callable(func):
                raise TypeError('Argument must be callable.')

            if func.__code__.co_argcount != self.param_num:
                raise TypeError(f"the delegate takes {self.param_num} positional arguments "
                                f"but you added {func.__code__.co_argcount}.")
            self.__func_list.append(func)

    def __call__(self, *args, **kwargs):  # 定义__call__方法
        """调用这个委托,返回委托内部的所有函数"""
        res_list = []
        if self.__func_list is []:
            return res_list
        for func in self.__func_list:
            temp = func(*args, **kwargs)
            # 只把有返回值的东西返回出去
            if temp is not None:
                res_list.append(temp)
        return tuple(res_list)

    def add(self, func):
        # 添加监听, 后续直接用重载+=运算符,下面类似
        if not callable(func):
            raise TypeError('Argument must be callable.')
        if self.param_num == -1:
            self.__func_list.append(func)
            self.param_num = func.__code__.co_argcount
            return

        if func.__code__.co_argcount != self.param_num:
            raise TypeError(f"the delegate takes {self.param_num} positional arguments "
                            f"but you added {func.__code__.co_argcount}.")

        self.__func_list.append(func)

    def remove(self, func):
        if func in self.__func_list:
            self.__func_list.remove(func)
        if len(self.__func_list) == 0:
            self.param_num = -1

    def __iadd__(self, func):
        self.add(func)
        return self

    def __isub__(self, func):
        self.remove(func)
        return self


class EventCenter:
    """事件中心"""
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__event_dic = {}

    def add_event_listener(self, name: str, action):
        if name in self.__event_dic:
            self.__event_dic[name] += action
        else:
            self.__event_dic[name] = Delegate(action)

    def RemoveEventListener(self, name: str, action):
        if name in self.__event_dic:
            self.__event_dic[name] -= action

    def event_trigger(self, name: str, *args, **kwargs):
        if name in self.__event_dic:
            self.__event_dic[name](*args, **kwargs)

    def delete_event(self, name: str):
        if name in self.__event_dic:
            del self.__event_dic[name]

    def clear(self):
        self.__event_dic = {}
