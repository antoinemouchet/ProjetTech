from sqlalchemy import Boolean, Column, DateTime, Integer, String, Model, ForeignKey
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
        

 
# cause each WatchList can contain more than 1 show.
class ShowList(Model):
    __tablename__ = 'show_lists'
			
    show_id = Column(Integer, ForeignKey('Show.id'), primary_key=True)
    watchlist_id = Column(Integer, ForeignKey('WatchList.id'), primary_key=True)       
                
                                
class WatchList(Model):
    __tablename__ = 'watch_lists'
			
    id = Column(Integer, primary_key=True, autoincrement=True)
    # show = Column(Integer, ForeignKey('Show.id'))  -> see ShowList
    user_id = Column(Integer, ForeignKey('Utilisateur.id'))
    # status : what is it ? xD


Base.metadata.create_all(engine)
