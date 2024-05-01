# app.py
from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from db import Database

db = Database('sqlite:///app.db')

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='SuperMarket')
spec.register(app)
from products import products
from departments import departments

app.register_blueprint(products)
app.register_blueprint(departments)

if __name__ == '__main__':
    app.run()
