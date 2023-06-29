import sqlalchemy
from sqlalchemy.orm import sessionmaker
#import psycopg2
from db_models import create_tables
from db_config import LOGIN, PASSWORD, DB_PORT, DB_NAME


#это временная заглушка, потом лишние точки входа уберем, просто пока сложновато
if __name__ == '__main__':
    DSN = f'postgresql://{LOGIN}:{PASSWORD}@localhost:{DB_PORT}/{DB_NAME}'
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

def add_bot_user():
    pass

def add_vk_users():
    pass

def delete_vk_users():
    pass

def add_favourite():
    pass

def add_photos():
    pass

def add_blacklist():
    pass