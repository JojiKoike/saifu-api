from rest_framework import viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from core.permissions import CustomPermissions


class ReadOnlyViewSetBase(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet Base for Master (ReadOnly)
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class AdminEditableViewSetBase(viewsets.ModelViewSet):
    """
    ViewSet Base for Master (ONLY Admin user Editable)
    """
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class IsOwnerOnlyViewSetBase(viewsets.ModelViewSet):
    """
    ViewSet Base for Transaction and User
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, CustomPermissions.IsOwnerOnlyFullAccess,)
