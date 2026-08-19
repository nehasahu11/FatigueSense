import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


MYSQL_URL = os.getenv(
    "MYSQL_URL",
    "mysql+pymysql://root:password@localhost:3306/fatiguesense"
)


engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()