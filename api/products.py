from flask import request, jsonify, Blueprint
from flask_pydantic_spec import Response
from app import spec, db
import models

products = Blueprint('products', __name__)


@products.route('/products', methods=['GET'])
def get_products():
    if request.method == 'GET':
        products = db.session.query(models.Product).all()
        s_products = [product.serialize() for product in products]

        return (
            jsonify({'message': 'All Found Products', 'data': s_products}),
            200,
        )

    else:
        return jsonify({'error': 'Method not allowed'}), 405


@products.route('/product/<int:id>', methods=['GET', 'DELETE'])
def get_product(id):
    if request.method == 'GET':
        product = db.session.query(models.Product).filter_by(id=id).first()
        if product:
            return (
                jsonify(
                    {'message': 'Found Product', 'data': product.serialize()}
                ),
                200,
            )
        else:
            return jsonify({'error': 'Product not found'}), 404
    elif request.method == 'DELETE':
        product = db.session.query(models.Product).filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
    else:
        return jsonify({'error': 'Method not allowed'}), 405


@products.route('/product', methods=['POST'])
@spec.validate(
    body=models.ProductModel, resp=Response(HTTP_201=models.ProductModel)
)
def post_product():
    if request.method == 'POST':
        data = request.context.body.dict()
        department = (
            db.session.query(models.Department)
            .filter_by(id=data.get('department_id'))
            .first()
        )
        if department:
            try:
                product = models.Product(**data)
            except:
                return jsonify({'message': 'Invalid Input Data'}), 400
        else:
            return jsonify({'message': 'Not Found Department ID'}), 404
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'POST Product', 'data': data})
    else:
        return jsonify({'error': 'Method not allowed'}), 405


@products.route('/product/<int:id>', methods=['PUT'])
@spec.validate(
    body=models.ProductModel, resp=Response(HTTP_201=models.ProductModel)
)
def put_product(id):
    if request.method == 'PUT':
        data = request.context.body.dict()
        product = db.session.query(models.Product).filter_by(id=id).first()
        department = (
            db.session.query(models.Department)
            .filter_by(id=data.get('department_id'))
            .first()
        )
        if product and department:
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.department_id = data.get(
                'department', product.department_id
            )
            db.session.commit()
            return (
                jsonify(
                    {
                        'message': f'Product {product.name} updated successfully',
                        'data': data,
                    }
                ),
                200,
            )
        else:
            return jsonify({'error': 'Product or Department not found'}), 404
