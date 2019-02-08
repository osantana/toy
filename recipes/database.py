from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_searchable import make_searchable


class Database:
    _instance = None

    def __init__(self):
        self.database_url = None
        self.engine = None
        self.connection = None
        self.session = None

        self.Model = declarative_base()
        self.Session = sessionmaker()

        make_searchable(self.Model.metadata)

    def init_app(self, application):
        self.database_url = application.config['database_url']
        self.connect(self.database_url, application.debug)
        application.extensions['db'] = self

    def connect(self, database_url, debug=False):
        self.engine = create_engine(database_url, echo=debug)
        self.Session.configure(bind=self.engine)
        self.connection = self.engine.connect()
        self.session = self.Session()

    def create_tables(self):
        return self.Model.metadata.create_all(self.engine)

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
