from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import starlette
from starlette.responses import RedirectResponse

import requests
import ast
from . import models, schemas
from .db_conection import SessionLocal, engine
import json

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
@app.get('/cars', response_model=List[schemas.Car])
def show_cars(db: SessionLocal = Depends(get_db)):
    return db.query(models.Car).all()


# Read by car_plate
@app.get('/cars/{car_plate}')
def read_cars_by_plate(car_plate: str, db: SessionLocal = Depends(get_db)):
    if car_plate:
        car_plate = {
            "car_plate": car_plate
        }
        data = requests.get(f'http://localhost:8080/dev/lambda_function/cars/{car_plate}')
        try:
            data = (data.content).decode('utf-8').replace("'", '"')
            data = json.loads(data)
            json_object = json.loads(data)
        except Exception as e:
            json_object = {
                "car_plate": "not_found",
                "car_name": "not_found",
            }
        return json_object
    else:
        return starlette.response.Response(status_code=404)
