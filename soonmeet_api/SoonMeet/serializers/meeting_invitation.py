from rest_framework import serializers
from rest_framework.validators import ValidationError

from SoonMeet.models import MeetingInvitation, UserProfile
from SoonMeet.utils.fcm_notification_sender import NotificationSender


class MeetingInvitationSerializer(serializers.ModelSerializer):
    """ Serializes meeting invitation. """

    class Meta:
        model = MeetingInvitation
        fields = ('id', 'inviting_user', 'invited_user', 'event_date', 'attendance_status', 'attendance_required',
                  'last_modified', 'meeting_title')
        extra_kwargs = {
            'inviting_user': {'read_only': True},
            'attendance_status': {'style': {'base_template': 'radio.html'}},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        invited_user = validated_data['invited_user']
        event_date = validated_data['event_date']

        if not isinstance(user, UserProfile):
            raise ValidationError('You have to be logged in in order to invite to meeting!')

        if MeetingInvitation.objects.filter(inviting_user=user, invited_user=invited_user, event_date=event_date):
            raise ValidationError('Meeting invitation from you to this person for this date has already been sent!')

        meeting_invitation = MeetingInvitation.objects.create(**validated_data, inviting_user=user)
        if user.id != invited_user.id:
            NotificationSender().send_notification(user_id=invited_user.id,
                                                   title='Zaproszenie na spotkanie',
                                                   message=f'Użytkownik {user.username} '
                                                           f'zaprasza Cię na spotkanie. Zobacz szczegóły w aplikacji.')
        return meeting_invitation
