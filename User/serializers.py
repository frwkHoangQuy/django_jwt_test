from rest_framework import serializers

from User.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [field.name for field in model._meta.fields if field.name != 'password']
