from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_engine = create_engine('sqlite:///scool.db', convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
)

Base = declarative_base()
Base.query = db_session.query_property()



def init_db():
    from model.comment import Comment
    from model.level import Level
    from model.staff import Staff
    from model.student import Student
    from model.company import Company
    from model.course import Course
    from model.transaction import Transaction, StudentTransaction, CompanyTransaction

    Base.metadata.create_all(bind=db_engine)
