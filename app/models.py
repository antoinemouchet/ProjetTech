from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./db.db", echo=True)
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


Base.metadata.create_all(engine)
