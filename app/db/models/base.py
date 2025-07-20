from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModelDB(Base):
    __abstract__ = True
