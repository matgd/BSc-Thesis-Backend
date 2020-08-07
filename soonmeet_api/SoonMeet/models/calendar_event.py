from django.db import models
from django.conf import settings

from SoonMeet.models import EventDate


class CalendarEvent(models.Model):
    """ Database model for user's calendar event. """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    event_date = models.ForeignKey(EventDate, related_name='event_date', on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=255, blank=True, null=True)
