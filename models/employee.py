from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Employee(Base):

    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    benefit_cost = Column(Integer, nullable=False)
