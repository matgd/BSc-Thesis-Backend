from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .api_client_user import APIClientUser


class TestCalendarEvent(APITestCase):
    """ Test /user_profile endpoint. """

    def setUp(self) -> None:
        self.client = APIClientUser()
        self.client.create_profile()
        self.client.login()

        event_type_id = self.client.post('/api/event_type/', {'name': 'DEFAULT', 'color': '#0000FF'}).data['id']
        event_date_data = {
            'type': event_type_id,
            'start_date': '2019-11-29T11:13:00Z',
            'end_date': '2019-11-29T13:13:00Z',
            'frequency': '',
            'location': 'test_town',
        }
        self.event_date_id = self.client.post('/api/event_date/', event_date_data).data['id']
        self.calendar_event_data = {'event_date': self.event_date_id, 'description': 'test'}

    def test_create_calendar_event(self):
        """ Test if creating calendar event returns HTTP 201 CREATED code. """
        response = self.client.post('/api/calendar_event/', self.calendar_event_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_calendar_event(self):
        """ Test if patching calendar event description returns 200 OK code."""
        post_response = self.client.post('/api/calendar_event/', self.calendar_event_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        patch_data = {'event_date': self.event_date_id, 'description': 'another_desc'}
        patch_response = self.client.patch(f'/api/calendar_event/{post_response.data["id"]}/', patch_data)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
