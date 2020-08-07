from rest_framework.pagination import LimitOffsetPagination

from SoonMeet.views import UserProfileViewSet


class LimitOffsetPaginationDefLimit5(LimitOffsetPagination):
    default_limit = 5


class UserProfilePaginationViewSet(UserProfileViewSet):
    """
    Handle creating and updating user profiles.
    Pagination by limit and offset.
    Search filter: search by providing phrase (?search=xyz)
    Search fields: username, first_name, last_name
    """
    pagination_class = LimitOffsetPaginationDefLimit5
