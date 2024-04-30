import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import *

class Database:

    def __init__(self, url):

        self.engine = sa.create_engine(url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()