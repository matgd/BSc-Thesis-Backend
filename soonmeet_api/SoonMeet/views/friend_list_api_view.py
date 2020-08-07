from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

from SoonMeet.models.friend_invitation import FriendInvitation


class FriendListApiView(APIView):
    """
    Returns JSON array containing authorized user's friends (is inviter or invitee and invitation is ACCEPTED).
    There is also ID of invitation which can come in handy for PATCH request.
    """
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        friend_ids_from_self_invites = [
            {
                'profile': invitation.invited_user.id,
                'username': invitation.invited_user.username,
                'first_name': invitation.invited_user.first_name,
                'last_name': invitation.invited_user.last_name,
                'invitation': invitation.id,
            } for invitation in FriendInvitation.objects.filter(
                Q(inviting_user_id=request.user.id) & Q(invitation_status=FriendInvitation.ACCEPTED)
            )
        ]
        friend_ids_from_external_invites = [
             {
                 'profile': invitation.inviting_user.id,
                 'username': invitation.inviting_user.username,
                 'first_name': invitation.inviting_user.first_name,
                 'last_name': invitation.inviting_user.last_name,
                 'invitation': invitation.id,
             } for invitation in FriendInvitation.objects.filter(
                Q(invited_user_id=request.user.id) & Q(invitation_status=FriendInvitation.ACCEPTED)
            )
        ]

        return Response(friend_ids_from_self_invites + friend_ids_from_external_invites)
