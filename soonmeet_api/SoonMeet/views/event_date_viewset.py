from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
import django_filters

from SoonMeet import serializers, models
from SoonMeet.permissions import SafeMethods


class EventDateFilter(django_filters.FilterSet):
    start_date__lte = django_filters.DateFilter(field_name='start_date', lookup_expr='lte')
    start_date__gte = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date__lt = django_filters.DateFilter(field_name='start_date', lookup_expr='lt')
    start_date__gt = django_filters.DateFilter(field_name='start_date', lookup_expr='gt')
    end_date__lte = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    end_date__gte = django_filters.DateFilter(field_name='end_date', lookup_expr='gte')
    end_date__lt = django_filters.DateFilter(field_name='end_date', lookup_expr='lt')
    end_date__gt = django_filters.DateFilter(field_name='end_date', lookup_expr='gt')

    class Meta:
        model = models.EventDate
        fields = [
            'start_date',
            'end_date',
            'frequency',
            'start_date__lte',
            'start_date__gte',
            'start_date__lt',
            'start_date__gt',
            'end_date__lte',
            'end_date__gte',
            'end_date__lt',
            'end_date__gt'
        ]


class EventDateViewSet(viewsets.ModelViewSet):
    """
    Handle creating and reading event date, time and location.
    GET List: all event dates
    Search filter: search by GET keyword arguments
    Search fields: start_date, end_date, start_time, end_time
    """
    serializer_class = serializers.EventDateSerializer
    queryset = models.EventDate.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (SafeMethods,)
    filter_class = EventDateFilter
