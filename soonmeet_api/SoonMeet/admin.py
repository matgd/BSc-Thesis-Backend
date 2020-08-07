from django.contrib import admin

from SoonMeet import models

admin.site.register(models.UserProfile)
admin.site.register(models.FriendInvitation)
admin.site.register(models.EventType)
admin.site.register(models.EventDate)
admin.site.register(models.CalendarEvent)
admin.site.register(models.MeetingInvitation)
