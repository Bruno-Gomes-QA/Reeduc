# app.py
from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from db import Database

db = Database('mysql+pymysql://root:toor@localhost:3306/base')

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Reciclagem API')
spec.register(app)
from products import products

app.register_blueprint(products)

if __name__ == '__main__':
    app.run()
