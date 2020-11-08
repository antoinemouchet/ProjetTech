from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Text
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


# cause each WatchList can contain more than 1 show.
class ShowList(Base):
    __tablename__ = 'showlists'

    show_id = Column(Integer, ForeignKey('show.id'), primary_key=True)
    watchlist_id = Column(Integer, ForeignKey(
        'watchlists.id'), primary_key=True)


Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()
