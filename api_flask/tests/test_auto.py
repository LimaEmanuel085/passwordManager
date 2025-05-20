import secrets
import string
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pytest import fixture
from scripts.app import app

def gen_password(length=12):
    char = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(char) for _ in range(length))
    return password
password = gen_password()

@fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hash_password_success(client):
    response = client.post('/hash', json={
        'password': password
    })
    assert response.status_code == 201
    data = response.get_json()
    assert password == data['password']
    assert data['hashed_password']

def test_verify_password_success(client):
    json = client.post('/hash', json={
        'password': password
    })
    assert json.status_code == 201
    data = json.get_json()
    response = client.post('/verify', json=data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['valid']

def test_hash_password_not_provided(client):
    response = client.post('/hash', json={'password': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Password is required'

def test_verify_password_not_provided(client):
    json = client.post('/hash', json={
        'password': password
    })
    assert json.status_code == 201
    data = json.get_json()
    response = client.post('/verify', json={
        'hashed_password': data['hashed_password']
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Password and hashed password are required'

def test_verify_hashed_not_provided(client):
    json = client.post('/hash', json={
        'password': password
    })
    assert json.status_code == 201
    data = json.get_json()
    response = client.post('/verify', json={
        'password': data['password']
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Password and hashed password are required'
