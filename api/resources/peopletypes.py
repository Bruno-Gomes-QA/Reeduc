# People Types endpoints similar people endpoints, but with different models and schemas
from flask import request, jsonify, Blueprint, g, current_app
from flask_pydantic_spec import Response, Request
from sqlalchemy.exc import SQLAlchemyError
from models import PeopleType
from schemas import PeopleTypeModel, PeopleTypeGet


peopletypes = Blueprint('peopletypes', __name__)


def create_people_types_blueprint(spec):
    @peopletypes.route('/peopletypes', methods=['GET'])
    @spec.validate(query=PeopleTypeGet)
    def get_people_types():
        db_session = g.db_session
        try:
            query = db_session.query(PeopleType)

            people_type_id = request.args.get('id')
            people_type_name = request.args.get('name')
            people_type_description = request.args.get('description')

            if people_type_id:
                query = query.filter(PeopleType.id == people_type_id)
            else:
                if people_type_name:
                    query = query.filter(
                        PeopleType.name.contains(people_type_name)
                    )
                if people_type_description:
                    query = query.filter(
                        PeopleType.description.contains(
                            people_type_description
                        )
                    )

            people_types = query.all()
            s_people_types = [
                people_type.serialize() for people_type in people_types
            ]
            return (
                jsonify(
                    {
                        'message': 'Filtered People Types',
                        'data': s_people_types,
                    }
                ),
                200,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    @peopletypes.route('/peopletype', methods=['POST'])
    @spec.validate(body=PeopleTypeModel)
    def create_people_type():
        db_session = g.db_session
        try:
            data = request.json
            people_type = PeopleType(**data)
            db_session.add(people_type)
            db_session.commit()
            return (
                jsonify({'message': 'People Type created', 'data': data}),
                201,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    @peopletypes.route('/peopletype/<int:id>', methods=['PUT'])
    @spec.validate(body=PeopleTypeModel)
    def update_people_type(id):
        db_session = g.db_session
        try:
            data = request.json
            db_session.query(PeopleType).filter(PeopleType.id == id).update(
                data
            )
            db_session.commit()
            return (
                jsonify({'message': 'People Type updated', 'data': data}),
                200,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    @peopletypes.route('/peopletype/<int:id>', methods=['DELETE'])
    def delete_people_type(id):
        db_session = g.db_session
        try:
            people_type = db_session.query(PeopleType).filter_by(id=id).first()
            if not people_type:
                return jsonify({'message': 'People Type not found'}), 404
            db_session.delete(people_type)
            db_session.commit()
            return (
                jsonify({'message': 'People Type deleted successfully'}),
                200,
            )
        except SQLAlchemyError as e:
            return (
                jsonify({'message': 'Error: {}'.format(e)}),
                500,
            )
        finally:
            db_session.close()

    return peopletypes
