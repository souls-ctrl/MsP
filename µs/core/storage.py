from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQLBase:
    """."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    tables = []
    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.tables.append(self.__tablename__)

    @declared_attr
    def __tablename__(self):
        """."""
        return self.__name__.lower()

Base = declarative_base(cls=SQLBase)


class SQLStorage:
    """."""
    def __init__(self, database_uri):
        """."""
        self.database_uri = database_uri
        self.engine = create_engine(self.database_uri, convert_unicode=True)
        self.session = None

    def __enter__(self):
        """."""
        session_maker = sessionmaker(bind=self.engine, expire_on_commit=True)
        self.session = session_maker()
        return self

    def __exit__(self, type_, value, traceback_):
        """."""
        _ = type_, value, traceback_
        is_success = True
        if type_ is not None or value is not None or traceback_ is not None:
            print(type_, value)
            is_success = False
        self.session.commit()
        self.session.close()
        return is_success
        
    def create_tables(self, tables):
        """."""
        Base.metadata.create_all(bind=self.engine, tables=tables)

    def create(self, table, items):
        """."""
        tuple_ = table.insert().values(**items)
        connection = self.engine.connect()
        connection.execute(tuple_)

    def read(self, table, **kwargs):
        """."""
        connection = self.engine.connect()
        if not kwargs:
            statement = table.select()
        else:
            statement = table.select().where()
        res = connection.execute(statement)
        return [dict(row) for row in res]

    def update(self):
        """."""
        pass

    def delete(self):
        """."""
        pass

if __name__ == '__main__':
    storage = SQLStorage('sqlite:///sqlite.db')
    print(storage)