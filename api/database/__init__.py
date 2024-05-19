import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base


class Database:
    def __init__(self, url):
        self.engine = sa.create_engine(url)
        Base.metadata.create_all(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.SessionFactory)

    def get_session(self):
        return self.Session()
