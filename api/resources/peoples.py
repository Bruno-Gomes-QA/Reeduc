# Similar route products.py, but with peoples endpoint
from flask import Blueprint, jsonify, request, current_app, g
from flask_pydantic_spec import Response, Request
from sqlalchemy.exc import SQLAlchemyError
from models import People
from schemas import PeopleModel, PeopleGet

peoples = Blueprint('peoples', __name__)


def create_peoples_blueprint(spec):
    @peoples.route('/peoples', methods=['GET'])
    @spec.validate(query=PeopleGet)
    def get_peoples():
        db_session = g.db_session
        try:
            query = db_session.query(People)
            people_id = request.args.get('people_id')
            name = request.args.get('name')
            email = request.args.get('email')
            tel = request.args.get('tel')
            cpf = request.args.get('cpf')
            status = request.args.get('status')
            people_type_id = request.args.get('people_type_id')

            if people_id:
                query = query.filter(People.id == people_id)
            else:
                if name:
                    query = query.filter(People.name.contains(name))
                if email:
                    query = query.filter(People.email.contains(email))
                if tel:
                    query = query.filter(People.tel.contains(tel))
                if cpf:
                    query = query.filter(People.cpf.contains(cpf))
                if status:
                    query = query.filter(People.status == status)
                if people_type_id:
                    query = query.filter(
                        People.people_type_id == people_type_id
                    )

            peoples = query.all()
            s_peoples = [people.serialize() for people in peoples]
            return (
                jsonify({'message': 'Filtered Peoples', 'data': s_peoples}),
                200,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    @peoples.route('/people', methods=['POST'])
    @spec.validate(body=PeopleModel)
    def create_people():
        db_session = g.db_session
        try:
            data = request.json
            people = People(**data)
            db_session.add(people)
            db_session.commit()
            return (
                jsonify({'message': 'People created', 'data': data}),
                201,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    @peoples.route('/people/<int:id>', methods=['PUT'])
    @spec.validate(body=Request(PeopleModel))
    def update_people(id):
        db_session = g.db_session
        try:
            data = request.json
            people = db_session.query(People).filter_by(id=id).first()
            if not people:
                return (
                    jsonify({'message': 'People not found'}),
                    404,
                )
            people.name = data.get('name', people.name)
            people.email = data.get('email', people.email)
            people.tel = data.get('tel', people.tel)
            people.cpf = data.get('cpf', people.cpf)
            people.status = data.get('status', people.status)
            people.people_type_id = data.get(
                'people_type_id', people.people_type_id
            )
            db_session.commit()
            return (
                jsonify({'message': 'People updated', 'data': data}),
                200,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    @peoples.route('/people/<int:id>', methods=['DELETE'])
    def delete_people(id):
        db_session = g.db_session
        try:
            people = db_session.query(People).filter_by(id=id).first()
            if not people:
                return (
                    jsonify({'message': 'People not found'}),
                    404,
                )
            db_session.delete(people)
            db_session.commit()
            return (
                jsonify({'message': 'People deleted'}),
                200,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    return peoples
