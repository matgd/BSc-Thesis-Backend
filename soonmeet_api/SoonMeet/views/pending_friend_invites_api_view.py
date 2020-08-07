from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

from SoonMeet.models.friend_invitation import FriendInvitation


class PendingFriendInvitesApiView(APIView):
    """ Returns list of objects containing
      * friend_invitation id
      * inviting_user id
      * friend_invitation invitation_status
      of authorized user where invitation is external and status is either ACCEPTED or SENT.
    """
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        pending_invites = [
            {
                'friend_invitation': invitation.id,
                'inviting_user': invitation.inviting_user.id,
                'invitation_status': invitation.invitation_status

            } for invitation in FriendInvitation.objects.filter(
                Q(invited_user_id=request.user.id) &
                (Q(invitation_status=FriendInvitation.READ) | Q(invitation_status=FriendInvitation.SENT))
            )
        ]
        return Response(pending_invites)
