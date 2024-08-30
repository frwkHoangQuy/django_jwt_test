import jwt
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from User.models import User
from UserTest import settings


class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        token = request.headers.get('Authorization')
        if token:
            try:
                token = token.replace('Bearer ', '')
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user_id = payload["user_id"]
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                request.user_permissions = []
        else:
            request.user_id = None
            request.user_permissions = []


class PermissionRequiredMixin:
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if request.user_id is None:
            return self.handle_no_permission()
        if request.user_id:
            user = User.objects.get(id=request.user_id)
            if user.is_active is None:
                return self.handle_no_permission()
        if self.permission_required and self.permission_required not in request.user_permissions:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        raise PermissionDenied("Bạn không có quyền truy cập.")
