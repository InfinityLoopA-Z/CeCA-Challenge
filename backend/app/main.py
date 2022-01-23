from typing import List
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


# Read
@app.get('/cars/', response_model=List[schemas.Car])
def show_cars(db: SessionLocal = Depends(get_db)):
    return db.query(models.Car).all()


# Read by car_plate
@app.get('/cars/{car_plate}', response_model=List[schemas.Car])
def read_cars_by_plate(car_plate: str, db: SessionLocal = Depends(get_db)):
    return db.query(models.Car).filter_by(car_plate=car_plate).all()
