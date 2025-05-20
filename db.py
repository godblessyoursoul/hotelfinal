from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "postgresql+psycopg2://postgres@localhost:5432/postgres" 

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-csearch_path=hotel"}
)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
