from rest_framework.permissions import BasePermission

class IsAuthenticatedAndActive(BasePermission):
    """
    Permite acesso apenas para usuários autenticados e ativos.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)
