from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///db.db?check_same_thread=false", echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    pseudo = Column(String)
    password = Column(String)
    enabled = Column(Boolean)
    authenticated = Column(Boolean)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.enabled

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Show(Base):
    # Table name
    __tablename__ = "show"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    desc = Column(Text, nullable=False)
    img = Column(Text)
    video = Column(Text)
    tags = Column(Text, nullable=False)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()
