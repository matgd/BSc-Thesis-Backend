from rest_framework import serializers

from SoonMeet import models


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile object. """

    class Meta:
        model = models.UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'last_modified', 'email', 'password')
        extra_kwargs = {  # custom configuration
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'email': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        """
        Create a new user.
        :param validated_data: dict: validated data
        :return: created user
        """
        user = models.UserProfile.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user
