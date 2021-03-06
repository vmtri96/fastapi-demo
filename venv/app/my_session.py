import sqlalchemy as db
import sqlalchemy.orm
from app.base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


my_session_maker: db.orm.session.sessionmaker = None

def initialize():
    global my_session_maker
    engine = db.create_engine("sqlite:///tiki_db", echo=True, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    my_session_maker = sessionmaker(bind=engine)


def get_session():
    session: db.orm.Session = my_session_maker()
    return session


async def get_db():
    session: db.orm.Session = my_session_maker()
    try:
        yield session
    finally:
        session.close()



