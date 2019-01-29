from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    _instance = None

    def __init__(self, connect_url, echo=False):
        self.connect_url = connect_url
        self.engine = create_engine(connect_url, echo=echo)
        self.connection = self.engine.connect()
        self.Model = declarative_base()

    @classmethod
    def get(cls, connect_url, echo=False):
        if cls._instance is None:
            cls._instance = cls(connect_url, echo=echo)
        return cls._instance
