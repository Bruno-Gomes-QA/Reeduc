# app.py
from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
import os
from db import Database

user = os.environ['USER']
password = os.environ['PASSWORD']
host = os.environ['HOST']
port = os.environ['PORT']
database = os.environ['DATABASE']
debug_mode = os.environ['DEBUG']

db = Database(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='API')
spec.register(app)
from products import products

app.register_blueprint(products)

if __name__ == '__main__':
    app.run(debug=debug_mode)
