from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import APP_CONF
from sqlalchemy.orm import declarative_base


db_engine = create_engine(APP_CONF.DB_URI)
db_session = sessionmaker(db_engine)  # expire_on_commit=False

Base = declarative_base()
