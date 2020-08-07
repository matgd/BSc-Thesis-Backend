from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework import status

from SoonMeet import serializers, models
from SoonMeet.permissions import UserIsInviterOrInvitee
from SoonMeet.models import FriendInvitation


class FriendInvitationViewSet(viewsets.ModelViewSet):
    """
    Handle creating and updating friend invitations.
    Search filter: search by providing GET keyword arguments
    Search fields: inviting_user, invited_user, sending_date, invitation_status

    PATCH only can change invitation status.

    For friend list go to /api/friend_list
    """
    serializer_class = serializers.FriendInvitationSerializer
    queryset = models.FriendInvitation.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserIsInviterOrInvitee,)
    filterset_fields = ['inviting_user', 'invited_user', 'sending_date', 'invitation_status']

    def partial_update(self, request, *args, **kwargs):
        inviting_user = request.data['inviting_user']
        invited_user = request.data['invited_user']

        user_is_inviter = request.user.id == inviting_user
        user_is_invitee = request.user.id == invited_user

        if user_is_invitee:
            if request.data['invitation_status'] not in (
                    FriendInvitation.ACCEPTED, FriendInvitation.REJECTED, FriendInvitation.READ):
                raise ValidationError('As invitee you can only mark invitation as ACCEPTED, REJECTED or READ.')

        if user_is_inviter:
            if request.data['invitation_status'] not in (FriendInvitation.REJECTED,):
                raise ValidationError('As inviter you can only mark invitation as REJECTED.')

        FriendInvitation.objects.filter(id=request.data['id']).update(
            invitation_status=request.data['invitation_status']
        )
        return Response(request.data, status.HTTP_202_ACCEPTED)
