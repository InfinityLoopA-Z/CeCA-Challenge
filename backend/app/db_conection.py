import os
from os.path import join

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
DOTENV_PATH = join(BASE_DIR, '.env')

config = load_dotenv(DOTENV_PATH)

engine = create_engine(
    os.environ.get("DATABASE_URL"),
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
