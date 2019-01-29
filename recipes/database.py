from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    _instance = None

    def __init__(self):
        self.database_url = None
        self.engine = None
        self.connection = None

        self.Model = declarative_base()

    def init_app(self, application):
        self.database_url = application.config['database_url']
        self.engine = create_engine(self.database_url, echo=application.debug)
        self.connection = self.engine.connect()

        application.extensions['db'] = self

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_db(application=None):
    database = Database.get()
    if application is not None:
        database.init_app(application)
    return database


db = get_db()
