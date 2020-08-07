from django.urls import path, include
from rest_framework.routers import DefaultRouter

from SoonMeet import views


router = DefaultRouter()
router.register('profile', views.UserProfileViewSet, 'profile')  # no base_name because of queryset inside
router.register('profile_pagination', views.UserProfilePaginationViewSet)
router.register('friend_invitation', views.FriendInvitationViewSet, 'friend_invitation')
router.register('event_type', views.EventTypeViewSet, 'event_type')
router.register('event_date', views.EventDateViewSet, 'event_date')
router.register('calendar_event', views.CalendarEventViewSet, 'calendar_event')
router.register('meeting_invitation', views.MeetingInvitationViewSet, 'meeting_invitation')

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('friend_list/', views.FriendListApiView.as_view()),
    path('pending_friend_invites/', views.PendingFriendInvitesApiView.as_view()),
    path('propose_meeting/', views.ProposeMeetingApiView.as_view()),
    path('user_email_password/', views.UserEmailPasswordApiView.as_view()),
    path('', include(router.urls))
]
