from pydantic import BaseModel


class Car(BaseModel):
    id: str
    car_name: str
    car_plate: str

    class Config:
        orm_mode = True
