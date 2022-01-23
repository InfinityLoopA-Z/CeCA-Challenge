import pymysql
import os
import json
from dotenv import load_dotenv

# read JSON file which is in the next parent folder
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
DOTENV_PATH = os.path.join(BASE_DIR, '.env')
config = load_dotenv(DOTENV_PATH)


file = os.path.join(BASE_DIR, 'script/example_db.json')

json_data = open(file).read()
json_obj = json.loads(json_data)


# do validation and checks before insert
def validate_string(val):
    if val is not None:
        if type(val) is int:
            return str(val).encode('utf-8')
        else:
            return val


db_name = os.environ.get('DB_NAME')

# connect to MySQL
try:
    con = pymysql.connect(
        host=os.environ.get('DATABASE_HOST'),
        user=os.environ.get('DATABASE_USER'),
        passwd=os.environ.get('DATABASE_PASSWORD'),
        db=db_name
    )
    cursor = con.cursor()
except Exception as e:
    print(e)

cursor.execute(f'DROP TABLE IF EXISTS {db_name}')
sql = f'''CREATE TABLE {db_name}(
   ID CHAR(36) NOT NULL,
   CAR_NAME CHAR(20),
   CAR_PLATE CHAR(6)
);'''

cursor.execute(sql)

# parse json data to SQL insert
for i, item in enumerate(json_obj):
    id = validate_string(item.get("id", None))
    car_name = validate_string(item.get('car_name', None))
    car_plate = validate_string(item.get('car_plate', None))
    sql = f'''INSERT INTO {db_name}(
        id, car_name, car_plate
        ) VALUES('{id}', '{car_name}', '{car_plate}')'''
    cursor.execute(sql)
con.commit()
con.close()
