from constants import DB_HOST, DB_USER, DB_PASS, DB_NAME

import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


connection = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
dbengine: Engine = sqlalchemy.create_engine(connection, pool_pre_ping=True)
Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    __table_args__ = {'schema': DB_NAME}

    workspace = Column("workspace", String(32), nullable=False, primary_key=True)
    forum = Column("forum", String(32), nullable=False)

    def __repr__(self):
        return "Course({0}, {1})".format(self.workspace, self.forum)
