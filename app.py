from db import engine
from models import Base

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("все создалось в схеме отель 'hotel'.")
