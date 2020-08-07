from django.db import models

from SoonMeet.models import EventType


class EventDate(models.Model):
    """ Database model regarding date, time and location of the calendar event. """
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    YEARLY = 'YEARLY'
    FREQUENCY_LIST = [
        (WEEKLY, WEEKLY),
        (MONTHLY, MONTHLY),
        (YEARLY, YEARLY)
    ]

    type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.CharField(
        max_length=7,
        choices=FREQUENCY_LIST,
        blank=True,
        null=True
    )
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_date__lte=models.F('end_date')),
                                   name='start_date_lte_end_date'),
        ]

    def __str__(self):
        return f'ID: {self.id} | ' \
               f'{self.start_date} - {self.end_date}, {self.location}'
