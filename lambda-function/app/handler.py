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
        return car_name.decode('utf-8')


# Save in redis cache a car plate and car name
def _store_redis(car_name, car_plate):
    redis_client.set(car_plate, car_name)
    return car_name


# Search in mysql db a car plate
def _search_db(db: SessionLocal, car_plate):
    try:
        get_db()
        car = db.query(models.Car).filter_by(car_plate=car_plate).all()
        return car.name if car else None
    except Exception as e:
        print(e)
        return None


def query_handler(event, context):
    if event is not None:
        car_plate = event
        car_name = _search_redis(car_plate)
        if car_name is None:
            car_name = _search_db(car_plate)
            _store_redis(car_plate, car_name)

        return car_name
    else:
        return json.dumps({'error': 'no event'})
# serverless invoke local --function hello --data 'Hello'
