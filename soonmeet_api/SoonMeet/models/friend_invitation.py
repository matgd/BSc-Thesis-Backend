from django.db import models
from django.conf import settings


class FriendInvitation(models.Model):
    """ Database model of user invitations. """
    SENT = 'SENT'
    READ = 'READ'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    INVITATION_STATUSES = [
        (SENT, SENT),  # first value is stored in DB, second one is human-readable
        (READ, READ),
        (ACCEPTED, ACCEPTED),
        (REJECTED, REJECTED)
    ]

    inviting_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inviting_user', on_delete=models.CASCADE)
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invited_user', on_delete=models.CASCADE)
    sending_date = models.DateTimeField(auto_now_add=True)
    invitation_status = models.CharField(
        max_length=8,
        choices=INVITATION_STATUSES,
        default=SENT
    )
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inviting_user', 'invited_user'], name='one_invitation'),
        ]
