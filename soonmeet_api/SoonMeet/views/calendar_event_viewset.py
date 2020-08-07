from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from SoonMeet import serializers, models
from SoonMeet.permissions import CreateOwnCalendarEvent


class CalendarEventViewSet(viewsets.ModelViewSet):
    """
    Create and modify events in user's calendar.
    GET List: all calendar events
    Search filter: search by GET keyword arguments
    Search fields: user, event_date, frequency
    """
    serializer_class = serializers.CalendarEventSerializer
    queryset = models.CalendarEvent.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CreateOwnCalendarEvent,)
    filterset_fields = ['user', 'event_date']
