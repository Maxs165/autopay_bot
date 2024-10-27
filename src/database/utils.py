from database.base import Base
from database.base import db_engine
from database.models import *


def init_db():
    Base.metadata.create_all(bind=db_engine)
