from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

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

    def check_password(self, password):
        return check_password_hash(self.password, password)


Base.metadata.create_all(engine)


@login_manager.user_loader
def load_user(userid):
    return session.query(User).get(int(userid))


Session = sessionmaker(engine)
session = Session()
