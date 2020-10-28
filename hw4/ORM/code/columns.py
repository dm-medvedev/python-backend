import datetime


class Column():
    """
    https://docs.python.org/3/howto/descriptor.html#validator-class
    """
    def __init__(self, inner_type):
        self._inner_type = inner_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return getattr(obj, f'_{self.name}')

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, f'_{self.name}', value)

    def validate(self, value):
        if not isinstance(value, self._inner_type):
            raise TypeError(f"can't set {self.__class__} with {type(value)}")


class Integer(Column):
    def __init__(self):
        super().__init__(int)


class Float(Column):
    def __init__(self):
        super().__init__(float)


class String(Column):
    def __init__(self):
        super().__init__(str)


class Boolean(Column):
    def __init__(self):
        super().__init__(bool)

    def __set__(self, obj, value):
        if isinstance(value, int):
            if value in {0, 1}:
                value = bool(value)
        self.validate(value)
        setattr(obj, f'_{self.name}', value)


class Date(Column):
    def __init__(self):
        super().__init__(datetime.date)

    def __set__(self, obj, value):
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        self.validate(value)
        setattr(obj, f'_{self.name}', value)
