from locust import HttpUser, task, between


class CarPriceUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post('/login',
            json={'username': 'admin', 'password': 'admin'},
            headers={'api-key': 'demo-key'}
        )
        self.token = response.json()['access_token']

    @task(3)
    def predict(self):
        self.client.post('/predict',
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
            headers={'api-key': 'demo-key', 'token': self.token}
        )

    @task(1)
    def login(self):
        self.client.post('/login',
            json={'username': 'admin', 'password': 'admin'},
            headers={'api-key': 'demo-key'}
        )
