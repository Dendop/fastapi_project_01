from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

if not load_dotenv():
    load_dotenv(dotenv_path='/home/dendop/.env') #for prod path


db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
#encoding the password, Linux struggle to work with special characters
db_password_encoded = quote_plus(db_password)

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_password_encoded}@{db_host}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()