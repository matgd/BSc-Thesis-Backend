from rest_framework import serializers


class EmailPasswordSerializer(serializers.Serializer):
    """ Serializer for changing email or password. """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
