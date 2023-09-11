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
        for func in self.__func_list:
            temp = func(*args, **kwargs)
            # 只把有返回值的东西返回出去
            if temp is not None:
                res_list.append(temp)
        return tuple(res_list)

    def Add(self, func):
        if not callable(func):
            raise TypeError('Argument must be callable.')

        if func.__code__.co_argcount != self.param_num:
            raise TypeError(f"the delegate takes {self.param_num} positional arguments "
                            f"but you added {func.__code__.co_argcount}.")

        self.__func_list.append(func)

    def Remove(self, func):
        if func in self.__func_list:
            self.__func_list.remove(func)

    def __iadd__(self, func):
        self.Add(func)
        return self

    def __isub__(self, func):
        self.Remove(func)
        return self
