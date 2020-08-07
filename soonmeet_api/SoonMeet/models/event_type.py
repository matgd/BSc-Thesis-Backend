from django.db import models
from django.core.validators import RegexValidator


class EventType(models.Model):
    """ Database model regarding type of the calendar event. """
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=7, validators=[
        RegexValidator(regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                       message='Incorrect color (must be hex code).')
    ])
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ID: {self.id} | {self.name}'
