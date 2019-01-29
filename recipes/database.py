from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        self.database_url = None
        self.engine = None
        self.connection = None

        self.Model = declarative_base()

    def init_app(self, application):
        self.database_url = application.config['database_url']
        self.engine = create_engine(self.database_url, echo=application.debug)
        self.connection = self.engine.connect()
