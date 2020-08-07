from rest_framework import serializers
from rest_framework.validators import ValidationError

from SoonMeet import models


class CalendarEventSerializer(serializers.ModelSerializer):
    """ Serializes user's calendar event. """

    class Meta:
        model = models.CalendarEvent
        fields = ('id', 'user', 'event_date', 'description', 'last_modified')
        extra_kwargs = {
            'user': {'read_only': True},
            'frequency': {'style': {'base_template': 'radio.html'}}
        }

    def create(self, validated_data):
        user = self.context['request'].user

        if not isinstance(user, models.UserProfile):
            raise ValidationError('You have to be logged in in order to invite!')

        calendar_event = models.CalendarEvent.objects.create(**validated_data, user=user)
        return calendar_event
