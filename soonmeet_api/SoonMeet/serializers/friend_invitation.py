from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError


from SoonMeet.models import FriendInvitation
from ..validators.not_equal import validate_not_equal
from SoonMeet.utils.fcm_notification_sender import NotificationSender


class FriendInvitationSerializer(serializers.ModelSerializer):
    """ Serializer for friend invitations. """

    class Meta:
        model = FriendInvitation
        fields = ('id', 'inviting_user', 'invited_user', 'sending_date', 'invitation_status', 'last_modified')
        extra_kwargs = {
            'invitation_status': {'style': {'base_template': 'radio.html'}}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=FriendInvitation.objects.all(),
                fields=['inviting_user', 'invited_user']
            )
        ]

    def create(self, validated_data):
        inviting_user = validated_data['inviting_user']
        invited_user = validated_data['invited_user']

        if self.context['request'].user.id != inviting_user.id:
            raise ValidationError('You can only send invites as yourself!')

        validate_not_equal(
            inviting_user.id,
            invited_user.id,
            'The fields inviting_user and invited_user cannot be the same.'
        )

        try:
            FriendInvitation.objects.get(invited_user=inviting_user, inviting_user=invited_user)
            raise ValidationError('Invited user already sent invitation to you.')
        except FriendInvitation.DoesNotExist:
            pass

        friend_invitation = FriendInvitation.objects.create(**validated_data)
        NotificationSender().send_notification(user_id=invited_user.id,
                                               title='Zaproszenie do znajomych',
                                               message=f'Użytkownik {inviting_user.username} '
                                                       f'zaprasza Cię do swojego grona znajomych!')

        return friend_invitation
