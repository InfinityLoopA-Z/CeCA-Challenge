from sqlalchemy import Column, Integer, String

from .db_conection import Base


class Car(Base):
    __tablename__ = "CECA"

    id: str = Column(String, primary_key=True, index=True)
    car_name: str = Column(String, unique=True, index=True)
    car_plate: str = Column(String, unique=True, index=True)
