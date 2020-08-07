from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework import status

from SoonMeet import serializers, models
from SoonMeet.permissions import UserIsInviterOrInvitee


class MeetingInvitationViewSet(viewsets.ModelViewSet):
    """
    Create and modify meeting invitations.
    Search filter: search by providing GET keyword arguments
    Search fields: inviting_user, invited_user, event_date, attendance_status, attendance_required
    """
    serializer_class = serializers.MeetingInvitationSerializer
    queryset = models.MeetingInvitation.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserIsInviterOrInvitee,)
    filterset_fields = ['inviting_user', 'invited_user', 'event_date', 'attendance_status', 'attendance_required']

    def partial_update(self, request, *args, **kwargs):
        inviting_user = request.data['inviting_user']
        invited_user = request.data['invited_user']

        user_is_inviter = request.user.id == inviting_user
        user_is_invitee = request.user.id == invited_user

        if user_is_inviter or user_is_invitee:
            if request.data['attendance_status'] not in (
                    STATUS for STATUS, DB_STATUS in models.MeetingInvitation.ATTENDANCE_STATUSES
            ):
                raise ValidationError('Attendance status is not correct.')

        models.MeetingInvitation.objects.filter(id=request.data['id']).update(
            attendance_status=request.data['attendance_status'],
            event_date=request.data['event_date'],
            meeting_title=request.data['meeting_title']
         )
        return Response(request.data, status.HTTP_202_ACCEPTED)
