
from sqlalchemy  import create_engine ,text 
from sqlalchemy.orm import Session ,sessionmaker,declarative_base
from app.core.config import settings
from contextlib import contextmanager
Base = declarative_base()

#create database engine 

engine = create_engine(
    settings.DATABASE_URL,

    pool_pre_ping = True ,
)

#create session factory (that create db session)

SessionLocal = sessionmaker(

    bind=engine , 
    autoflush =False,
    autocommit=False
)

def create_table():
    Base.metadata.create_all(bind=engine)

#using in each endpoint for create db session
def get_db():
    db =SessionLocal()#factory pattern create instance from class so using ()
    try:        # i have connection bool (set of db connection each connection uder  without colse that is not return to pool)
        yield db  # to give me one session (db connection)for each request and wait until query is end
    finally: # to close connection after query 
        db.close()


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()