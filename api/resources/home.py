# Home my api flask

from flask import request, jsonify, Blueprint, g, current_app

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def get_home():
    return (
        jsonify({'message': 'Bem-vindo a API da Reeduc'}),
        200,
    )
