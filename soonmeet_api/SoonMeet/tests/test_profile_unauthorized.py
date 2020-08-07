from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase


class TestProfileUnauthorized(APITestCase):
    """ Test /user_profile endpoint. """

    def setUp(self) -> None:
        self.client = Client()
        self.profile_data = {
            'username': 'TesterNovember5',
            'password': 'qweasdzxc',
            'first_name': 'Testq',
            'last_name': 'Testr',
            'email': 'testqr5@gmail.com'
        }

    def test_create_profile(self):
        """ Test if creating profile returns HTTP 201 CREATED code. """
        response = self.client.post('/api/profile/', self.profile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_profile_already_taken_username(self):
        """ Test if creating profile with already taken username returns HTTP 400 BAD REQUEST code."""
        response_1st = self.client.post('/api/profile/', self.profile_data)
        self.assertEqual(response_1st.status_code, status.HTTP_201_CREATED)
        response_2nd = self.client.post('/api/profile/', self.profile_data)
        self.assertEqual(response_2nd.status_code, status.HTTP_400_BAD_REQUEST)

