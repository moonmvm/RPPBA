from rest_framework import (
    decorators,
    status,
    response,
    mixins,
    viewsets,
)

from .serializers import WarehouseSerializer, CellSerializer
from .models import Warehouse, Cell


class WarehouseViewSet(viewsets.GenericViewSet):
    serializer_class = WarehouseSerializer

    @decorators.action(
        methods=['GET'],
        detail=False,
        url_path='warehouse',
    )
    def get_warehouse(self, request):
        warehouse = Warehouse.load()
        serializer = self.get_serializer(warehouse)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class CellViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    serializer_class = CellSerializer
    queryset = Cell.objects.all()

    @decorators.action(
        methods=['GET'],
        detail=False,
        url_path='empty-cells',
    )
    def get_empty_cells(self, request):
        empty_cells = self.get_queryset().filter(actual_size=0)
        serializer = self.get_serializer(empty_cells, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
