from flask import Flask, g
from flask_pydantic_spec import FlaskPydanticSpec
import os
from dotenv import load_dotenv
from database import Database
from resources.products import create_products_blueprint
from resources.departments import create_departments_blueprint
from resources.users import create_users_blueprint
from resources.peoples import create_peoples_blueprint
from resources.peopletypes import create_people_types_blueprint
from resources.home import home


def create_app(testing=False):

    load_dotenv()

    app = Flask(__name__)
    if testing:
        print('Testing')
        app.config[
            'SQLALCHEMY_DATABASE_URI'
        ] = 'mysql+pymysql://user:toor@localhost:3306/base'
    else:
        user = os.environ['USERMYSQL']
        password = os.environ['PASSWORD']
        host = os.environ['HOST']
        port = os.environ['PORT']
        data = os.environ['DATABASE']
        app.config[
            'SQLALCHEMY_DATABASE_URI'
        ] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{data}'

    db = Database(app.config['SQLALCHEMY_DATABASE_URI'])

    spec = FlaskPydanticSpec('flask', title='Reeduc API')
    spec.register(app)
    app.db = db
    app.register_blueprint(create_products_blueprint(spec))
    app.register_blueprint(create_departments_blueprint(spec))
    app.register_blueprint(create_users_blueprint(spec))
    app.register_blueprint(create_peoples_blueprint(spec))
    app.register_blueprint(create_people_types_blueprint(spec))
    app.register_blueprint(home)

    @app.before_request
    def before_request():
        g.db_session = app.db.get_session()

    @app.teardown_request
    def teardown_request(exception=None):
        db_session = g.pop('db_session', None)
        if db_session is not None:
            db_session.close()

    return app
