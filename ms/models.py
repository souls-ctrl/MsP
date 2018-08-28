from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from ms.core.storage import Base
from ms.core.storage import SQLStorage


class Model:
    def __init__(self, tablename, **kwargs):
        """."""
        self.__tablename__ = tablename
        for name, value in kwargs.items():
            setattr(self, name, value)

    def to_dict(self):
        """."""
        return self.__dict__

    def to_table(self):
        """."""
        if self.__tablename__ not in Base.metadata.tables:
            table = type(self.__tablename__, (Base, ), self.to_dict()).__table__
        else:
            table = Base.metadata.tables[self.__tablename__]
        return table

    def add(self, items):
        """."""
        table = self.to_table()
        with SQLStorage("sqlite:///sqlite.db") as db:
            db.create(table, items)

    def get(self, str_fn=None):
        """."""
        table = self.to_table()
        with SQLStorage("sqlite:///sqlite.db") as db:
            return db.read(table)

    def __eq__(self, model):
        """."""
        return self.__tablename__ == model.__tablename__

    def __ne__(self, model):
        """."""
        return not self.__eq__(model)

    def __hash__(self):
        """."""
        return hash(self.__tablename__)

    def __str__(self):
        """."""
        return '<Model: %s>' % str(self.__dict__)

    def __repr__(self):
        """."""
        return str(self)

def text_field(max_length, **kwargs):
    """."""
    return Column(String(max_length), **kwargs)


def integer_field(**kwargs):
    """."""
    return Column(Integer, **kwargs)

def datetime_field(flag_timezone, **kwargs):
    """."""
    return Column(DateTime(timezone=flag_timezone), **kwargs)

Time = func

if __name__ == '__main__':
    model = Model('Product', price=250)
    tables = []
    tables.append(model)
    tables.append(model)
    print(tables)
    print(list(set(tables)))
