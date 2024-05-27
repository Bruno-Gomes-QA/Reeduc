from flask import request, jsonify, Blueprint, g, current_app
from flask_pydantic_spec import Response, Request
from sqlalchemy.exc import SQLAlchemyError
from models import Department
from schemas import DepartmentModel


def create_departments_blueprint(spec):
    departments = Blueprint('departments', __name__)

    @departments.route('/departments', methods=['GET'])
    def get_departments():
        db_session = g.db_session
        try:
            departments = db_session.query(Department).all()
            s_departments = [
                department.serialize() for department in departments
            ]
            return (
                jsonify({'message': 'All Departments', 'data': s_departments}),
                200,
            )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Failed to fetch departments: {e}')
            return jsonify({'error': 'Database error'}), 500

    @departments.route('/department', methods=['POST'])
    @spec.validate(body=Request(DepartmentModel))
    def post_department():
        db_session = g.db_session
        try:
            data = request.context.body.dict()
            department = Department(**data)
            db_session.add(department)
            db_session.commit()
            return (
                jsonify(
                    {
                        'message': 'Department added',
                        'data': department.serialize(),
                    }
                ),
                201,
            )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Failed to add department: {e}')
            return (
                jsonify({'message': 'Invalid Input Data', 'error': str(e)}),
                400,
            )

    @departments.route('/department/<int:id>', methods=['PUT'])
    @spec.validate(body=Request(DepartmentModel))
    def put_department(id):
        db_session = g.db_session
        try:
            data = request.context.body.dict()
            department = db_session.query(Department).filter_by(id=id).first()
            if not department:
                return jsonify({'error': 'Department not found'}), 404
            department.department_name = data.get(
                'department_name', department.department_name
            )
            db_session.commit()
            return (
                jsonify(
                    {
                        'message': 'Department updated',
                        'data': department.serialize(),
                    }
                ),
                200,
            )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Failed to update department: {e}')
            return jsonify({'error': 'Database error'}), 500

    @departments.route('/department/<int:id>', methods=['DELETE'])
    def delete_department(id):
        db_session = g.db_session
        try:
            department = db_session.query(Department).filter_by(id=id).first()
            if not department:
                return jsonify({'error': 'Department not found'}), 404
            db_session.delete(department)
            db_session.commit()
            return (
                jsonify({'message': 'Department deleted successfully'}),
                200,
            )
        except SQLAlchemyError as e:
            current_app.logger.error(f'Failed to delete department: {e}')
            return jsonify({'error': 'Database error'}), 500

    return departments
