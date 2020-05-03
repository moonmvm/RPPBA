from rest_framework import (
    decorators,
    status,
    response,
    mixins,
    viewsets,
)

from . import serializers
from .models import Nomenclature, Product
from warehouse.models import Cell
from warehouse.serializers import CellSerializer
from utils import constants


class NomenclatureViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    serializer_class = serializers.NomenclatureSerializer
    queryset = Nomenclature.objects.all()


class ProductViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = serializers.ProductReadOnlySerializer
    queryset = Product.objects.all()

    @decorators.action(
        methods=['POST'],
        detail=False,
        url_path='create-product',
    )
    def create_product(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=status.HTTP_201_CREATED)

    @decorators.action(
        methods=['GET'],
        detail=False,
        url_path='raw-materials',
    )
    def get_raw_materials(self, request):
        raw_materials_queryset = self.queryset.filter(
            nomenclature__nomenclature_type=constants.NomenclatureType.RAW_MATERIAL.value,
        )
        serializer = self.get_serializer(raw_materials_queryset, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=['GET'],
        detail=False,
        url_path='products',
    )
    def get_products(self, request):
        raw_materials_queryset = self.queryset.filter(
            nomenclature__nomenclature_type=constants.NomenclatureType.PRODUCT.value,
        )
        serializer = self.get_serializer(raw_materials_queryset, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=['POST'],
        detail=True,
        url_path='move-unsorted-product',
    )
    def move_product(self, request, pk=None):
        product = self.get_object()
        serializer = serializers.MoveProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        new_cell = Cell.objects.get(pk=serializer.validated_data['new_cell_id'])
        if amount <= product.amount:
            product.cell.add(new_cell)
            product.amount -= amount
            new_cell.actual_size += amount
            new_cell.save()
            product.save()
            return response.Response(status=status.HTTP_200_OK)
        return response.Response(
            data={'error': 'Amount should be <= than product amount'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @decorators.action(
        methods=['POST'],
        detail=True,
        url_path='move-sorted-product',
    )
    def move_sorted_product(self, request, pk=None):
        product = self.get_object()
        serializer = serializers.MoveProductFromCellSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_sell = Cell.objects.get(pk=serializer.validated_data['current_cell_id'])
        new_cell = Cell.objects.get(pk=serializer.validated_data['new_cell_id'])
        amount = serializer.validated_data['amount']
        if current_sell in product.cell.all():
            if amount <= current_sell.actual_size:
                product.cell.add(new_cell)
                new_cell.actual_size += amount
                current_sell.actual_size -= amount
                if current_sell.actual_size == 0:
                    product.cell.remove(current_sell)
                product.save()
                new_cell.save()
                current_sell.save()
                return response.Response(status=status.HTTP_200_OK)
            return response.Response(
                data='Amount should be <= than current cell actual size',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response.Response(
            data={'error': 'The product does not have such cell'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @decorators.action(
        methods=['POST'],
        detail=True,
        url_path='send-materials-to-manufacture',
    )
    def send_materials_to_manufacture(self, request, pk=None):
        product = self.get_object()
        if product.nomenclature.nomenclature_type == constants.NomenclatureType.RAW_MATERIAL.value:
            serializer = serializers.SendMaterialsToManufactureSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            amount = serializer.validated_data['amount']
            cell = Cell.objects.get(pk=serializer.validated_data['cell_id'])
            if cell in product.cell.all() and amount <= product.amount:
                cell.actual_size -= amount
                product.amount -= amount
                cell.save()
                product.save()
                return response.Response(status=status.HTTP_200_OK)
            return response.Response(
                data={'error': 'Product does not have such cell'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response.Response(data={'error': 'Must be raw material'}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        methods=['GET'],
        detail=True,
        url_path='cells',
    )
    def get_product_cells(self, request, pk=None):
        cells = self.get_object().cell.all()
        serializer = CellSerializer(cells, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
