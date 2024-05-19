from flask import request, jsonify, Blueprint, g, current_app
from flask_pydantic_spec import Response, Request
from sqlalchemy.exc import SQLAlchemyError
from models import Product, Department
from schemas import ProductModel, ProductGet

products = Blueprint('products', __name__)


def safe_convert_float(value):
    try:
        return float(value)
    except:
        return None


def create_products_blueprint(spec):
    @products.route('/products', methods=['GET'])
    @spec.validate(query=ProductGet)
    def get_products():
        db_session = g.db_session
        try:
            query = db_session.query(Product)

            product_name = request.args.get('product_name')
            product_description = request.args.get('product_description')
            department_id = request.args.get('department_id')
            buy_price = safe_convert_float(request.args.get('buy_price'))
            sale_price = safe_convert_float(request.args.get('sale_price'))
            stock = safe_convert_float(request.args.get('stock'))

            if department_id:
                query = query.filter(Product.department_id == department_id)
            if sale_price and sale_price >= 0:
                query = query.filter(Product.sale_price >= sale_price)
            elif sale_price and sale_price < 0:
                query = query.filter(Product.sale_price <= abs(sale_price))
            if buy_price and buy_price >= 0:
                query = query.filter(Product.buy_price >= buy_price)
            elif buy_price and buy_price < 0:
                query = query.filter(Product.buy_price <= abs(buy_price))
            if product_name:
                query = query.filter(
                    Product.product_name.contains(product_name)
                )
            if product_description:
                query = query.filter(
                    Product.product_description.contains(product_description)
                )
            if stock and stock >= 0:
                query = query.filter(Product.stock >= stock)
            elif stock and stock < 0:
                query = query.filter(Product.stock <= abs(stock))

            products = query.all()
            s_products = [product.serialize() for product in products]
            return (
                jsonify({'message': 'Filtered Products', 'data': s_products}),
                200,
            )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Failed to fetch products: {e}')
            return jsonify({'error': 'Database error'}), 500

    @products.route('/product/<int:id>', methods=['GET', 'DELETE'])
    def get_or_delete_product(id):
        db_session = g.db_session
        try:
            product = db_session.query(Product).filter_by(id=id).first()
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            if request.method == 'GET':
                return (
                    jsonify(
                        {
                            'message': 'Found Product',
                            'data': product.serialize(),
                        }
                    ),
                    200,
                )
            elif request.method == 'DELETE':
                db_session.delete(product)
                db_session.commit()
                return (
                    jsonify({'message': 'Product deleted successfully'}),
                    200,
                )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Error processing request: {e}')
            return jsonify({'error': 'Database error'}), 500

    @products.route('/product', methods=['POST'])
    @spec.validate(body=Request(ProductModel))
    def post_product():
        db_session = g.db_session
        try:
            data = request.context.body.dict()
            department = (
                db_session.query(Department)
                .filter_by(id=data.get('department_id'))
                .first()
            )
            if not department:
                return jsonify({'message': 'Department not found'}), 404

            product = Product(**data)
            db_session.add(product)
            db_session.commit()
            return (
                jsonify(
                    {'message': 'Product added', 'data': product.serialize()}
                ),
                201,
            )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Failed to add product: {e}')
            return (
                jsonify({'message': 'Invalid Input Data', 'error': str(e)}),
                400,
            )

    @products.route('/product/<int:id>', methods=['PUT'])
    @spec.validate(body=Request(ProductModel))
    def put_product(id):
        db_session = g.db_session
        try:
            data = request.context.body.dict()
            product = db_session.query(Product).filter_by(id=id).first()
            department = (
                db_session.query(Department)
                .filter_by(id=data.get('department_id'))
                .first()
            )
            if not product or not department:
                return (
                    jsonify({'error': 'Product or Department not found'}),
                    404,
                )

            product.product_name = data.get(
                'product_name', product.product_name
            )
            product.buy_price = data.get('buy_price', product.buy_price)
            product.sale_price = data.get('sale_price', product.sale_price)
            product.stock = data.get('stock', product.stock)
            product.product_description = data.get(
                'product_description', product.product_description
            )
            product.department_id = data.get(
                'department_id', product.department_id
            )

            db_session.commit()
            return (
                jsonify(
                    {
                        'message': 'Product updated successfully',
                        'data': product.serialize(),
                    }
                ),
                200,
            )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Failed to update product: {e}')
            return jsonify({'error': 'Database error'}), 500

    return products
