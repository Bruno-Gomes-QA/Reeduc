from flask import request, jsonify, Blueprint, current_app
from flask_pydantic_spec import Response, Request
from sqlalchemy.exc import SQLAlchemyError
from app import spec, db
from models import Product, Department
from schemas import ProductModel

products = Blueprint('products', __name__)

@products.route('/products', methods=['GET'])
def get_products():
    #GET All Products
    try:
        products = db.session.query(Product).all()
        s_products = [product.serialize() for product in products]
        return jsonify({'message': 'All Found Products', 'data': s_products}), 200
    except SQLAlchemyError as e:
        current_app.logger.error(f'Failed to fetch products: {e}')
        return jsonify({'error': 'Database error'}), 500

@products.route('/product/<int:id>', methods=['GET', 'DELETE'])
def get_or_delete_product(id):
    #GET or DELETE Product
    try:
        product = db.session.query(Product).filter_by(id=id).first()
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        if request.method == 'GET':
            return jsonify({'message': 'Found Product', 'data': product.serialize()}), 200
        elif request.method == 'DELETE':
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200
    except SQLAlchemyError as e:
        current_app.logger.error(f'Error processing request: {e}')
        return jsonify({'error': 'Database error'}), 500

@products.route('/product', methods=['POST'])
@spec.validate(body=Request(ProductModel), resp=Response(HTTP_201=ProductModel))
def post_product():
    #Create new Product
    try:
        data = request.context.body.dict()
        department = db.session.query(Department).filter_by(id=data.get('department_id')).first()
        if not department:
            return jsonify({'message': 'Department not found'}), 404

        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added', 'data': product.serialize()}), 201
    except SQLAlchemyError as e:
        current_app.logger.error(f'Failed to add product: {e}')
        return jsonify({'message': 'Invalid Input Data', 'error': str(e)}), 400

@products.route('/product/<int:id>', methods=['PUT'])
@spec.validate(body=Request(ProductModel), resp=Response(HTTP_200=ProductModel))
def put_product(id):
    #Update Product
    try:
        data = request.context.body.dict()
        product = db.session.query(Product).filter_by(id=id).first()
        department = db.session.query(Department).filter_by(id=data.get('department_id')).first()
        if not product or not department:
            return jsonify({'error': 'Product or Department not found'}), 404

        product.product_name = data.get('product_name', product.product_name)
        product.buy_price = data.get('buy_price', product.buy_price)
        product.sale_price = data.get('sale_price', product.sale_price)
        product.stock = data.get('stock', product.stock)
        product.product_description = data.get('product_description', product.product_description)
        product.department_id = data.get('department_id', product.department_id)

        db.session.commit()
        return jsonify({'message': 'Product updated successfully', 'data': product.serialize()}), 200
    except SQLAlchemyError as e:
        current_app.logger.error(f'Failed to update product: {e}')
        return jsonify({'error': 'Database error'}), 500
