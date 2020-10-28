from .columns import Column
from .utils import get_logger


logger = get_logger(__name__)


class MetaBase(type):
    """
    идея __table__ из
    https://lectureswww.readthedocs.io/6.www.sync/\
    2.codding/9.databases/2.sqlalchemy/3.orm.html

    само добавление из
    https://realpython.com/python-metaclasses/#custom-metaclasses
    и
    https://github.com/sqlalchemy/sqlalchemy/blob/\
    10851b002844fa4f9de7af92dbb15cb1133497eb/lib/\
    sqlalchemy/orm/decl_api.py#L54
    """
    def __new__(cls, name, bases, dct):
        base = super().__new__(cls, name, bases, dct)
        base.__table__ = {}
        base.__tablename__ = name.lower()
        for attr, value in base.__dict__.items():
            if isinstance(value, Column):
                base.__table__[attr] = value
        if name != 'Base':
            msg = ','.join(f'{k} ({v._inner_type})'
                           for k, v in base.__table__.items())
            logger.info(f"Created '{name}' class; "
                        f"columns: {msg}")
        return base


class Base(metaclass=MetaBase):
    def __init__(self, **kwargs):
        self._primary_dict = None
        tab_colums = set(self.__table__.keys())
        given_columns = set(kwargs.keys())
        if given_columns != tab_colums:
            diff1 = given_columns.difference(tab_colums)
            diff2 = tab_colums.difference(given_columns)
            s1 = f'columns do not exist: {diff1}' \
                 if len(diff1) > 0 else ''
            s2 = f'you missed to fill columns: {diff2}' \
                 if len(diff2) > 0 else ''
            raise AttributeError(' ;'.join((_ for _ in
                                 [s1, s2] if len(_) > 0)))
        for name, val in kwargs.items():
            try:
                setattr(self, name, val)
            except TypeError as ex:
                logger.error(f"Error in '{self.__class__.__name__}'"
                             f" instance while setting '{val}' to "
                             f"'{name}': '{ex}'")
            # здесь используем set

    def create(self):
        """
        create new row

        return None
        """
        columns = self.__table__.keys()
        values = tuple(getattr(self, c) for c in columns)
        connection = self.__session__.connection
        if not self.__session__.table_exists(self.__tablename__):
            self.__session__.create_table(self.__tablename__, columns)
        if self.row_exists(columns, values):
            raise RuntimeError("Can't create already existing row")
        connection.execute(f"INSERT INTO {self.__tablename__} "
                           f"({', '.join(columns)}) VALUES"
                           f"({', '.join('?'*len(columns))});", values)
        self._primary_dict = {k: v for k, v in zip(columns, values)}
        connection.commit()

    @classmethod
    def read(cls, **kwargs):
        """
        read existing rows

        return: List[Instance]
        """
        connection = cls.__session__.connection
        tab_colums = list(cls.__table__.keys())
        columns, values = zip(*kwargs.items())
        command = f"SELECT {', '.join(tab_colums)}" + \
                  f" FROM {cls.__tablename__} WHERE " + \
                  ' AND '.join(f'{c}=?' for c in columns) + ";"
        rows = list(connection.execute(command, values))
        primary_dicts = [{k: v for k, v in zip(tab_colums, r)} for r in rows]
        res = []
        for d in primary_dicts:
            obj = cls(**d)
            obj._primary_dict = d
            res.append(obj)
        return res

    @classmethod
    def all(cls):
        """
        read existing rows

        return: List[Instance]
        """
        connection = cls.__session__.connection
        tab_colums = list(cls.__table__.keys())
        command = f"SELECT {', '.join(tab_colums)}" + \
                  f" FROM {cls.__tablename__};"
        rows = list(connection.execute(command))
        primary_dicts = [{k: v for k, v in zip(tab_colums, r)} for r in rows]
        res = []
        for d in primary_dicts:
            obj = cls(**d)
            obj._primary_dict = d
            res.append(obj)
        return res

    def update(self):
        """
        update existing row

        return None
        """
        connection = self.__session__.connection
        if self._primary_dict is None:
            raise RuntimeError("Can't update non-readen or non-created row")
        wh_columns, wh_values = zip(*self._primary_dict.items())
        set_columns = list(self.__table__.keys())
        set_values = list(getattr(self, c) for c in set_columns)
        if not self.row_exists(wh_columns, wh_values):
            raise RuntimeError("Can't update non-existing row")
        if self.row_exists(set_columns, set_values):
            raise RuntimeError("Can't update row, update will create copy")
        command = f"UPDATE {self.__tablename__} SET " + \
                  ', '.join(f'{c}=?' for c in set_columns) + " WHERE " + \
                  ' AND '.join(f'{c}=?' for c in wh_columns) + ";"
        connection.execute(command, list(set_values) + list(wh_values))
        self._primary_dict = {c: v for c, v in zip(set_columns, set_values)}
        connection.commit()

    def delete(self):
        """
        delete existing row

        return None
        """
        connection = self.__session__.connection
        if self._primary_dict is None:
            raise RuntimeError("Can't delete non-readen or non-created row")
        columns, values = zip(*self._primary_dict.items())
        if not self.row_exists(columns, values):
            raise RuntimeError("Can't delete non-existing row")
        command = f"DELETE FROM {self.__tablename__} WHERE " + \
                  ' AND '.join(f'{c}=?' for c in columns) + ";"
        connection.execute(command, values)
        self._primary_dict = None
        connection.commit()
        # здесь используем get

    def row_exists(self, columns, values):
        connection = self.__session__.connection
        command = f"SELECT {', '.join(columns)}" + \
                  f" FROM {self.__tablename__} WHERE " + \
                  ' AND '.join(f'{c}=?' for c in columns) + ";"
        res = list(connection.execute(command, values))
        return len(res) != 0
