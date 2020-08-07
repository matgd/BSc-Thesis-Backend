from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile. """

    def has_object_permission(self, request, view, obj):
        """
        Grants permission when using safe methods, additional unsafe if user's profile.
        :param request: request
        :param view: view
        :param obj: object
        :return: bool: permission
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class SafeMethods(permissions.BasePermission):
    """ Safe methods (GET, POST, PUT, etc.) permission. """

    def has_object_permission(self, request, view, obj):
        """
        Grants read-only permission.
        :param request: request
        :param view: view
        :param obj: object
        :return: bool: True if method is read-only
        """

        return request.method in permissions.SAFE_METHODS


class UserIsInviterOrInvitee(permissions.BasePermission):
    """ Sending friend request can be only done in the name of logged in user. """

    def has_object_permission(self, request, view, obj):
        """
        Grants permission to inviter to read, invitee can read
        :param request: request
        :param view: view
        :param obj: object
        :return: bool: granted permission
        """
        user_is_inviter = obj.inviting_user.id == request.user.id
        user_is_invitee = obj.invited_user.id == request.user.id

        if user_is_inviter or user_is_invitee:
            inviter_methods = ('POST', 'PATCH', 'DELETE')
            invitee_methods = ('PATCH', 'DELETE')

            if user_is_inviter and request.method in inviter_methods:
                return True
            elif user_is_invitee and request.method in invitee_methods:
                return True

            if request.method in permissions.SAFE_METHODS:
                return True

        return False


class CreateOwnCalendarEvent(permissions.BasePermission):
    """ Allow users create and modify their own calendar event, rest can only read."""

    def has_object_permission(self, request, view, obj):
        """
        Grants permission when using safe methods, additional unsafe if user's profile.
        :param request: request
        :param view: view
        :param obj: object
        :return: bool: permission
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id
