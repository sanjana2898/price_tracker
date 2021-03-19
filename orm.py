import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float,Boolean,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
class Products(Base):

    __tablename__ ="products"

    id =Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    deal = Column(Boolean)
    url = Column(String)
    date = Column(DateTime, default=datetime.utcnow)  
    website = Column(String, default='amazon')  

if __name__ == "__main__":
    engine = create_engine('sqlite:///trackdb.sqlite3')
    Base.metadata.create_all(engine)