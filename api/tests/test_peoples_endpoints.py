from main import app
from pytest import fixture, mark

@fixture(scope='session')
def client():
    with app.test_client() as client:
        yield client

def test_given_not_peoples(client):
    response = client.get('/peoples')
    assert response.status_code == 200
    assert response.json == {'message': 'Filtered Peoples', 'data': []}
