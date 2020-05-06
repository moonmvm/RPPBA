from rest_framework import (
    decorators,
    status,
    permissions,
    response,
    viewsets,
)

from .serializers import LoginSerializer


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = None

    @decorators.action(
        methods=['POST'],
        detail=False,
        url_path='login',
        permission_classes=[permissions.AllowAny],
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.validated_data, status.HTTP_200_OK)
