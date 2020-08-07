from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .api_client_user import APIClientUser


class TestProfileAuthorized(APITestCase):
    """ Test /user_profile endpoint. """

    def setUp(self) -> None:
        self.client = APIClientUser()
        self.profile_data = {
            'username': 'TesterNovember5',
            'password': 'qweasdzxc',
            'first_name': 'Testq',
            'last_name': 'Testr',
            'email': 'testqr5@gmail.com'
        }

    def test_delete_profile(self):
        """ Test if deleting profile returns HTTP 204 NO CONTENT code. """
        response_create = self.client.create_profile()
        self.client.login()
        response_delete = self.client.delete(f'/api/profile/{response_create.data["id"]}/')
        self.client.logout()
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def __patch_profile(self, field: str, new_value: str):
        response_create = self.client.create_profile()
        patch_data = {
            'id': response_create.data['id'],
            'username': response_create.data['username'],
            'first_name': response_create.data['first_name'],
            'last_name': response_create.data['last_name'],
            field: new_value
        }
        self.client.login()
        response_patch = self.client.patch(f'/api/profile/{response_create.data["id"]}/', patch_data)
        self.client.logout()
        return response_patch

    def test_patch_profile_username(self):
        """ Test if patching profile username returns HTTP 200 OK code. """
        response_patch = self.__patch_profile('username', 'TesterNov0')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

    def test_patch_profile_first_name(self):
        """ Test if patching profile first name returns HTTP 200 OK code. """
        response_patch = self.__patch_profile('first_name', 'TestQ')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

    def test_patch_profile_last_name(self):
        """ Test if patching profile last name returns HTTP 200 OK code. """
        response_patch = self.__patch_profile('last_name', 'TestR')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
