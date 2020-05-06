from rest_framework import serializers, exceptions

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user_queryset = User.objects.filter(email=email)

        if not user_queryset.exists():
            raise exceptions.ValidationError('No such user')

        user = user_queryset.first()

        if user_queryset.exists and user_queryset.first().password != password:
            raise exceptions.ValidationError('Invalid password provided')

        validated_dict = {
            'id': user.pk,
            'token': user.auth_token.key,
        }
        return validated_dict
