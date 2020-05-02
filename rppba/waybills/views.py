from rest_framework import (
    decorators,
    status,
    response,
    mixins,
    viewsets,
)

from . import serializers
from .models import Clientele, Waybill


class ClienteleViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):
    serializer_class = serializers.ClienteleSerializer
    queryset = Clientele.objects.all()


class WaybillViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    serializer_class = serializers.WaybillReadOnlySerializer
    queryset = Waybill.objects.all()

    @decorators.action(
        methods=['POST'],
        detail=False,
        url_path='create-waybill',
    )
    def create_waybill(self, request):
        serializer = serializers.WaybillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=status.HTTP_201_CREATED)
