from rest_framework import serializers

from SoonMeet import models
from SoonMeet.validators.start_date_time_before_end_date_time import validate_start_before_end


class EventDateSerializer(serializers.ModelSerializer):
    """ Serializes an event date, time and location. """

    class Meta:
        model = models.EventDate
        fields = ('id', 'type', 'start_date', 'end_date', 'frequency', 'location', 'last_modified')
        extra_kwargs = {
            'frequency': {'style': {'base_template': 'radio.html'}}
        }
