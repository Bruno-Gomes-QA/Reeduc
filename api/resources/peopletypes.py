#People Types endpoints similar people endpoints, but with different models and schemas
from flask import request, jsonify, Blueprint, g, current_app
from flask_pydantic_spec import Response, Request
from sqlalchemy.exc import SQLAlchemyError
from models import PeopleType
from schemas import PeopleTypeModel

peopletypes = Blueprint('peopletypes', __name__)

def create_people_types_blueprint(spec):
  @peopletypes.route('/peopletypes', methods=['GET'])
  @spec.validate(query=PeopleTypeModel)
  def get_people_types():
    db_session = g.db_session
    try:
      query = db_session.query(PeopleType)

      name = request.args.get('name')
      description = request.args.get('description')

      if name:
        query = query.filter(PeopleType.name.contains(name))
      if description:
        query = query.filter(PeopleType.description.contains(description))

      people_types = query.all()
      s_people_types = [people_type.serialize() for people_type in people_types]
      return (
        jsonify({'message': 'Filtered People Types', 'data': s_people_types}),
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