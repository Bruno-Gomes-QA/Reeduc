import os
import pytest
from app import create_testing_app
from models import Base, Product, Department
from flask import json


@pytest.fixture(scope='module')
def test_client():

    flask_app = create_testing_app()
    flask_app.config['TESTING'] = True

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def setup_database():

    app = create_testing_app()
    session = app.db.get_session()

    Base.metadata.create_all(bind=app.db.engine)

    department = Department(
        name='Test Department', description='Test Description'
    )
    session.add(department)
    session.commit()

    product = Product(
        product_name='Test Product',
        product_description='Test Description',
        buy_price=10.0,
        sale_price=20.0,
        stock=100,
        department_id=department.id,
    )
    session.add(product)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=app.db.engine)


def test_get_products(test_client, setup_database):
    response = test_client.get('/products')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 1
    assert data['data'][0]['product_name'] == 'Test Product'


def test_get_product(test_client, setup_database):
    response = test_client.get('/product/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['product_name'] == 'Test Product'


def test_get_nonexistent_product(test_client, setup_database):
    response = test_client.get('/product/999')
    assert response.status_code == 404


def test_post_product(test_client, setup_database):
    new_product = {
        'product_name': 'New Product',
        'product_description': 'New Description',
        'buy_price': 15.0,
        'sale_price': 30.0,
        'stock': 50,
        'department_id': 1,
    }
    response = test_client.post('/product', json=new_product)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['product_name'] == 'New Product'


def test_put_product(test_client, setup_database):
    updated_product = {
        'product_name': 'Updated Product',
        'product_description': 'Updated Description',
        'buy_price': 20.0,
        'sale_price': 40.0,
        'stock': 200,
        'department_id': 1,
    }
    response = test_client.put('/product/1', json=updated_product)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['product_name'] == 'Updated Product'


def test_delete_product(test_client, setup_database):
    response = test_client.delete('/product/1')
    data = json.loads(response.data)
    assert data['message'] == 'Product deleted successfully'

    response = test_client.get('/product/1')
    assert response.status_code == 200
    assert response.status_code == 404
