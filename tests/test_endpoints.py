from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_success():
    response = client.post('/login',
        json={'username': 'admin', 'password': 'admin'},
        headers={'api-key': 'demo-key'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_login_invalid_credentials():
    response = client.post('/login',
        json={'username': 'wrong', 'password': 'wrong'},
        headers={'api-key': 'demo-key'}
    )
    assert 'error' in response.json()


def test_login_missing_api_key():
    response = client.post('/login',
        json={'username': 'admin', 'password': 'admin'}
    )
    assert response.status_code == 403


def test_predict():
    login = client.post('/login',
        json={'username': 'admin', 'password': 'admin'},
        headers={'api-key': 'demo-key'}
    )
    token = login.json()['access_token']

    response = client.post('/predict',
        json={
            'company': 'Maruti',
            'year': 2018,
            'km_driven': 50000,
            'fuel': 'Petrol',
            'seller_type': 'Individual',
            'transmission': 'Manual',
            'owner': 'First',
            'mileage_mpg': 45.0,
            'engine_cc': 1200.0,
            'max_power_bhp': 80.0,
            'torque_nm': 110.0,
            'seats': 5.0
        },
        headers={'api-key': 'demo-key', 'token': token}
    )
    assert response.status_code == 200
