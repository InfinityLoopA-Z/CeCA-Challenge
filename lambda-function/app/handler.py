import json
import redis
import os

from .db_connection import SessionLocal, engine
from . import models

redis_client = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=os.environ['REDIS_PORT'],
    db=0
)


# Connect to Db dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Search in redis cache a car plate
def _search_redis(car_plate):
    car_name = redis_client.get(car_plate)
    if car_name is None:
        return None
    else:
        car = {
            'car_name': car_name,
            'car_plate': car_plate
        }
        return car


# Save in redis cache a car plate and car name
def _save_redis(car_name, car_plate):
    redis_client.set(car_plate, car_name)
    car = {
        'car_name': car_name,
        'car_plate': car_plate
    }
    return json.dump(car)


# Search in mysql db a car plate
def _search_db(db: SessionLocal, car_plate):
    try:
        get_db()
        car = db.query(models.Car).filter_by(car_plate=car_plate).all()
        return car if car else None
    except Exception as e:
        print(e)
        return None


def get_car(event, context):
    if event is not None:
        car_plate = event
        car_redis = _search_redis(car_plate)
        if car_redis is None:
            car_db = _search_db(car_plate)
            if car_db is not None:
                _save_redis(car_db.car_plate, car_db.car_name)
                car = json.dumps(car_db.__dict__)
                return car
            else:
                car = json.dumps({'error': 'car not found'})
        else:
            car = json.dumps(car_redis)
            return car
    else:
        return json.dumps({'error': 'no event'})
