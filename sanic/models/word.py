import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True)
    rus = Column(String(255), nullable=False)
    heb = Column(String(255), nullable=False)
    type = Column(Integer, default=0)

    def __init__(self, rus, heb):
        self.uuid = str(uuid.uuid4())
        self.rus = rus
        self.heb = heb

    def __repr__(self):
        return f'Word({self.uuid}, {self.rus}, {self.heb})'
