from django.db import models
from django.conf import settings

from SoonMeet.models import EventDate


class MeetingInvitation(models.Model):
    """ Database model for meeting invitation. """
    SENT = 'SENT'
    READ = 'READ'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    ATTENDANCE_STATUSES = [
        (SENT, SENT),
        (READ, READ),
        (ACCEPTED, ACCEPTED),
        (REJECTED, REJECTED)
    ]

    inviting_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      related_name='meeting_inviting_user',
                                      on_delete=models.CASCADE)
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     related_name='meeting_invited_user',
                                     on_delete=models.CASCADE)
    event_date = models.ForeignKey(EventDate, related_name='meeting_event_date', on_delete=models.CASCADE)
    attendance_status = models.CharField(
        max_length=8,
        choices=ATTENDANCE_STATUSES,
        default=SENT
    )
    attendance_required = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    meeting_title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inviting_user', 'invited_user', 'event_date'],
                                    name='one_invitation_per_date'),
        ]
