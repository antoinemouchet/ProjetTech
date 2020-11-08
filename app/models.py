from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


class WatchParty(Base):
    __tablename__ = "watchparty"
    id = Column(String, primary_key=True)
    time = Column(Float)
    state = Column(Boolean)


class WatchPartyParameters(Base):
    __tablename__ = "watchpartyparameters"
    id = Column(String, ForeignKey('watchparty.id'), primary_key=True)
    type = Column(Boolean)  # True  => public  -> Blacklist
    # False => private -> Whitelist


class WatchPartyBlackList(Base):
    __tablename__ = "watchpartyparametersblacklist"
    id = Column(Integer, primary_key=True)
    parameters = Column(String, ForeignKey(
        'watchpartyparameters.id'))
    user = Column(Integer, ForeignKey('users.id'))


Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()
