from rest_framework import status
from rest_framework.test import APIClient


class APIClientUser(APIClient):
    def __init__(self, profile_data: dict = None):
        super().__init__()
        if profile_data:
            self.profile_data = {**profile_data}
        else:
            self.profile_data = {
                'username': 'TesterNovember5',
                'password': 'qweasdzxc',
                'first_name': 'Testq',
                'last_name': 'Testr',
                'email': 'testqr5@gmail.com'
            }

    def create_profile(self):
        response_create = self.post('/api/profile/', self.profile_data)
        assert response_create.status_code == status.HTTP_201_CREATED
        return response_create

    def login(self):
        response_login = self.post('/api/login/', {
            'username': self.profile_data['username'],
            'password': self.profile_data['password']
        })
        assert response_login.status_code == status.HTTP_200_OK
        token = response_login.data['token']
        self.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        return response_login

    def logout(self):
        self.credentials()
