from app import create_app
from pytest import fixture, mark
from models import Base

app = create_app(testing=True)
@fixture(scope='session')
def client():
    with app.test_client() as client:
        yield client
        Base.metadata.drop_all(app.db.engine)


def test_given_not_peoples_when_get_all_peoples_then_empty_data(client):
    response = client.get('/peoples')
    assert response.status_code == 201
    assert response.json == {'message': 'Filtered Peoples', 'data': []}


def test_given_not_people_types_when_post_people_then_error(client):
    data = {
        'name': 'Gandalf da Silva',
        'email': 'mago.supremo@gmail.com',
        'tel': '21999999999',
        'cpf': '12345678901',
        'status': 1,
        'people_type_id': 1,
    }
    response = client.post('/people', json=data)
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid People Type'}


def test_given_post_type_people(client):
    data = {'name': 'Test', 'description': 'Test'}
    response = client.post('/peopletype', json=data)
    assert response.status_code == 201
    assert response.json == {'message': 'People Type created', 'data': data}


def test_given_post_people(client):
    data = {
        'name': 'Gandalf da Silva',
        'email': 'mago.supremo@gmail.com',
        'tel': '21999999999',
        'cpf': '12345678901',
        'status': 1,
        'people_type_id': 1,
    }
    response = client.post('/people', json=data)
    assert response.status_code == 201
    assert response.json == {'message': 'People created', 'data': data}
