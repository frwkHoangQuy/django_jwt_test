from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Middleware.jwt_middleware import PermissionRequiredMixin
from .models import User
from .serializers import UserSerializer


class UserList(APIView, PermissionRequiredMixin):
    def get(self, request):
        query_set = User.objects.all()
        data = UserSerializer(query_set, many=True)
        return Response(data.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {}
        data["username"] = request.data["username"]
        data["password"] = make_password(request.data["password"])
        new_user = UserSerializer(data=data)
        if new_user.is_valid():
            new_user.save()
            return Response(new_user.data, status=status.HTTP_201_CREATED)
        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)
