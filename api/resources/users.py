from flask import request, jsonify, Blueprint, g, current_app
from flask_pydantic_spec import Response, Request
from sqlalchemy.exc import SQLAlchemyError
from models import User
from schemas import UserModel, UserGet

users = Blueprint('users', __name__)
def create_users_blueprint(spec):
  @users.route('/users', methods=['GET'])
  @spec.validate(query=UserGet)
  def get_users():
    db_session = g.db_session
    try:
      query = db_session.query(User)

      name = request.args.get('name')
      email = request.args.get('email')
      tel = request.args.get('tel')

      if name:
        query = query.filter(User.name.contains(name))
      if email:
        query = query.filter(User.email.contains(email))
      if tel:
        query = query.filter(User.tel.contains(tel))

      users = query.all()
      s_users = [user.serialize() for user in users]
      return jsonify({'message': 'Filtered Users', 'data': s_users}), 200
    except SQLAlchemyError as e:
      return jsonify({'message': 'Error', 'data': str(e)}), 500
    finally:
      db_session.close()


  @users.route('/users', methods=['POST'])
  @spec.validate(body=UserModel)
  def create_user():
    db_session = g.db_session
    try:
      user = User(**request.json)
      db_session.add(user)
      db_session.commit()
      return jsonify({'message': 'User created', 'data': user.serialize()}), 201
    except SQLAlchemyError as e:
      db_session.rollback()
      return jsonify({'message': 'Error', 'data': str(e)}), 500
    finally:
      db_session.close()

  return users 