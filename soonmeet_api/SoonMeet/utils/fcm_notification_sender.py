"""
Handling push notifications for phone.
Only for 1 person to use, for their project.
"""


import json
import requests
import os

DEFAULT_URL = 'https://fcm.googleapis.com/fcm/send'
DEFAULT_FCM_KEY = '*** REMOVED ***'

USER_ID__FCM_TOKEN = {
    int(os.environ.get('FMC_USER_ID', '*** REMOVED ***')): os.environ.get('FCM_TOKEN', '*** REMOVED ***')
}


class NotificationSender:
    """ Class handling push notifications. """
    def __init__(self, fcm_key: str = DEFAULT_FCM_KEY, url: str = DEFAULT_URL):
        """
        Constructor.
        :param fcm_key: FCM key taken from Google
        :param url: url to Google endpoint where POST requests are sent
        """
        self.url = url
        self.headers = {
            'content-type': 'application/json',
            'Authorization': f'key={fcm_key}'
        }

    def send_notification(self, user_id: int, title: str, message: str) -> bool:
        """
        Send notification with usage of Google FCM.
        :param user_id: user ID
        :param title: title of notification
        :param message: body of notification
        :return: notification has been sent
        """
        if user_id in USER_ID__FCM_TOKEN.keys():
            message_body = {
                'to': USER_ID__FCM_TOKEN[user_id],
                'notification': {
                    'title': title,
                    'body': message,
                }
            }
            requests.post(self.url, headers=self.headers, data=json.dumps(message_body))
            return True

        return False
