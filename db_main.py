import sqlalchemy
from sqlalchemy.orm import sessionmaker
import psycopg2
from models import create_tables

login = 'postgres'
password = 'Danil367173'
DSN = f'postgresql://{login}:{password}@localhost:5432/Bot_VK'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()