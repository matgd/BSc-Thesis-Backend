from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication

from SoonMeet import serializers, models
from SoonMeet.permissions import SafeMethods


class EventTypeViewSet(viewsets.ModelViewSet):
    """
    Handle creating and updating event types.
    GET List: all event types
    Search filter: search by providing phrase (?search=xyz)
    Search fields: name, color
    """
    serializer_class = serializers.EventTypeSerializer
    queryset = models.EventType.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (SafeMethods,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'color']
