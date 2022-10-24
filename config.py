import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DBNAME = os.environ.get('POSTGRES_DBNAME')
PORT = os.environ.get('POSTGRES_PORT')
IP = os.environ.get('POSTGRES_IP')


engine = create_engine(
    f'postgresql+psycopg2://{USER}:{PASSWORD}@{IP}:{PORT}/{DBNAME}')

base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Session.configure(bind=engine)

session = Session()
data_obj = MetaData(bind=engine)
