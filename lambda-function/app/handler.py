import json
import redis
import os

from dotenv import load_dotenv


from .db_connection import SessionLocal, engine, DOTENV_PATH
from . import models

config = load_dotenv(DOTENV_PATH)

redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    password=os.environ.get('REDIS_PASSWORD'),
    db=os.environ.get('REDIS_DB')
)


# Connect to Db dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def _get_car_plate(event: str):
    value = event['pathParameters']['car_plate']
    json_acceptable_string = value.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    return d['car_plate']


# Search in redis cache a car plate
def _search_redis(car_plate):
    car_name = redis_client.get(car_plate)
    if car_name is None:
        return None
    else:
        print("found in redis cache")
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
    print("saved in redis cache")
    return car


# Search in mysql db a car plate
def _search_db(car_plate):
    db = SessionLocal()
    try:
        get_db()
        car = db.query(models.Car).filter_by(car_plate=car_plate).first()
        return car if car else None
    except Exception as e:
        print(e)
        return None


def get_car(event, context):
    if event is not None:
        car_plate = _get_car_plate(event)
        car_redis = _search_redis(car_plate)
        if car_redis is None:
            car_db = _search_db(car_plate)
            if car_db is not None:
                _save_redis(car_db.car_name, car_plate)
                resp = {
                    'car_name': getattr(car_db, 'car_name'),
                    'car_plate': getattr(car_db, 'car_plate')
                }
                resp_json = json.dumps(resp)
                return resp_json
            else:
                return {
                    'error': 'Car not found'
                }
        else:
            car_name = car_redis['car_name'].decode('utf-8')
            car_plate = car_redis['car_plate']
            resp = {
                'car_name': car_name,
                'car_plate': car_plate
            }
            resp_json = json.dumps(resp)
            return resp_json
    else:
        return json.dumps({'error': 'no event'})
