# app.py
from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='SuperMarket')
spec.register(app)
from products import products
app.register_blueprint(products)

if __name__ == '__main__':
    app.run()