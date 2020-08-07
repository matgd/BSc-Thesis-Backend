from rest_framework import serializers

from SoonMeet import models


class EventTypeSerializer(serializers.ModelSerializer):
    """ Serializes an event type. """

    class Meta:
        model = models.EventType
        fields = ('id', 'name', 'color', 'last_modified')
