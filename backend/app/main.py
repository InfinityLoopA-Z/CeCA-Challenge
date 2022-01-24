from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from . import models, schemas
from .db_conection import SessionLocal, engine

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect to Db dependency
# get_lambda function dependency
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
@app.get('/car', response_model=List[schemas.Car])
def show_cars(db: SessionLocal = Depends(get_db)):
    return db.query(models.Car).all()


# Read by car_plate
@app.get('/cars/{car_plate}', response_model=List[schemas.Car])
def read_cars_by_plate(car_plate: str, db: SessionLocal = Depends(get_db)):
    return db.query(models.Car).filter_by(car_plate=car_plate).all()
