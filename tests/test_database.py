from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from app.main import app
from app.database import get_db,Base


load_dotenv()
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME') #+ '_test'
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_password_encoded = quote_plus(db_password)

#dont forget to create database with postgresql
SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_password_encoded}@{db_host}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
