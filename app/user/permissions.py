from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class IsSellerOrAdmin(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.has_role('seller') or request.user.has_role('admin'))
