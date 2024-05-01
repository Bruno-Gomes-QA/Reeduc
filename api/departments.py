from flask import request, jsonify, Blueprint
from flask_pydantic_spec import Response
from app import spec, db
import models

departments = Blueprint('departments', __name__)


@departments.route('/departments', methods=['GET'])
def get_departments():
    if request.method == 'GET':
        departments = db.session.query(models.Department).all()
        s_departments = [department.serialize() for department in departments]

        return (
            jsonify({'message': 'All Found Departments', 'data': s_departments}),
            200,
        )

    else:
        return jsonify({'error': 'Method not allowed'}), 405


@departments.route('/department/<int:id>', methods=['GET', 'DELETE'])
def get_department(id):
    if request.method == 'GET':
        department = db.session.query(models.Department).filter_by(id=id).first()
        if department:
            return (
                jsonify(
                    {'message': 'Found Department', 'data': department.serialize()}
                ),
                200,
            )
        else:
            return jsonify({'error': 'Department not found'}), 404
    elif request.method == 'DELETE':
        department = db.session.query(models.Department).filter_by(id=id).first()
        if department:
            db.session.delete(department)
            db.session.commit()
            return jsonify({'message': 'Department deleted successfully'}), 200
        else:
            return jsonify({'message': 'Department ID Not Found'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405


@departments.route('/department', methods=['POST'])
@spec.validate(
    body=models.DepartmentModel, resp=Response(HTTP_201=models.DepartmentModel)
)
def post_department():
    if request.method == 'POST':
        data = request.context.body.dict()
        try:
            department = models.Department(**data)
        except:
            return jsonify({'message': 'Invalid Input Data'}), 400
        db.session.add(department)
        db.session.commit()
        return jsonify({'message': 'POST Department', 'data': data})
    else:
        return jsonify({'error': 'Method not allowed'}), 405


@departments.route('/department/<int:id>', methods=['PUT'])
@spec.validate(
    body=models.DepartmentModel, resp=Response(HTTP_201=models.DepartmentModel)
)
def put_department(id):
    if request.method == 'PUT':
        data = request.context.body.dict()
        department = db.session.query(models.Department).filter_by(id=id).first()
        if department: 
            department.name = data.get('name', department.name)
            db.session.commit()
            return (
                jsonify(
                    {
                        'message': f'Department {department.name} updated successfully',
                        'data': data,
                    }
                ),
                200,
            )
        else:
            return jsonify({'error': 'Department not found'}), 404
    else:
        return jsonify({'error': 'Method not allowed'}), 405
