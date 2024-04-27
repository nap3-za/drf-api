from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsNotAuthenticated(BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_authenticated)


PERMITTED_CRITERIA = [
	"OPTION_ONE",
    "OPTION_TWO",
]

class IsPermittedCriteria(BasePermission):
    """
    Allows access permitted criteria.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.account_type in PERMITTED_CRITERIA)

