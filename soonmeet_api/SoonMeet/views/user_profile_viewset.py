from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from SoonMeet import serializers, models, permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Handle creating and updating user profiles.
    GET List: all user profiles
    Search filter: search by providing phrase (?search=xyz)
    Search fields: username, first_name, last_name
    """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name')

