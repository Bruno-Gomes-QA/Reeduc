#Similar route products.py, but with peoples endpoint
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

            name = request.args.get('name')
            email = request.args.get('email')
            tel = request.args.get('tel')
            cpf = request.args.get('cpf')
            status = request.args.get('status')
            people_type_id = request.args.get('people_type_id')

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
                query = query.filter(People.people_type_id == people_type_id)

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

    return peoples