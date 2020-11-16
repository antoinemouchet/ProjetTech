from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Text, Float
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


@login_manager.user_loader
def load_user(userid):
    return session.query(User).get(int(userid))


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


class WatchList(Base):
    __tablename__ = 'watchlists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # show = Column(Integer, ForeignKey('Show.id'))  -> see ShowList
    user_id = Column(Integer, ForeignKey('users.id'))
    # status : what is it ? xD


class ShowList(Base):
    __tablename__ = 'showlists'

    show_id = Column(Integer, ForeignKey('show.id'), primary_key=True)
    watchlist_id = Column(Integer, ForeignKey(
        'watchlists.id'), primary_key=True)


class FriendShip(Base):
    __tablename__ = 'friendship'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_a = Column(Integer, ForeignKey('users.id'))
    user_b = Column(Integer, ForeignKey('users.id'))


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
