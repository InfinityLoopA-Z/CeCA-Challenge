from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse

from . import models, schemas
from .db_conection import SessionLocal, engine

app = FastAPI()


# Connect to Db dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs")


# Create
@app.post("/car", response_model=schemas.Car)
def create_car(car: schemas.Car, db: SessionLocal = Depends(get_db)):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


# Read
@app.get('/cars/')
def read_cars(
    skip: int = 0,
    limit: int = 100,
    db: SessionLocal = Depends(get_db)
):
    cars = db.query(models.Car).offset(skip).limit(limit).all()
    return [
            {
                "id": car.id,
                "car_name": car.car_name,
                "car_plate": car.car_plate
            } for car in cars
    ]


# Read by car_plate
@app.get('/cars/{car_plate}', response_model=schemas.Car)
def read_cars_by_plate(car_plate: str, db: SessionLocal = Depends(get_db)):
    car = db.query(models.Car).filter(
                                    models.Car.car_plate == car_plate).first()
    if car:
        return {
            "id": car.id,
            "car_name": car.car_name,
            "car_plate": car.car_plate
        }
    return {"detail": "Car not found"}


# Update
@app.put("/car/{car_id}", response_model=schemas.Car)
def update_car(
    car_id: str,
    car: schemas.Car,
    db: SessionLocal = Depends(get_db)
):
    db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if db_car:
        db_car.car_name = car.car_name
        db_car.car_plate = car.car_plate
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car
    return None


# Delete
@app.delete("/car/{car_id}", response_model=schemas.Car)
def delete_car(
    car_id: str,
    db: SessionLocal = Depends(get_db)
):
    db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if db_car:
        db.delete(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car
    return None
