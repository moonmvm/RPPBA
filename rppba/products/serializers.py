from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from warehouse.serializers import CellSerializer
from warehouse.models import Cell
from .models import Nomenclature, Product


class NomenclatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nomenclature
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReadOnlySerializer(ProductSerializer):
    cell = CellSerializer(required=False, many=True)
    nomenclature = NomenclatureSerializer()


class MoveProductSerializer(serializers.Serializer):
    new_cell_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate(self, data):
        amount = data.get('amount')
        cell_queryset = Cell.objects.filter(pk=data.get('new_cell_id'))
        if not cell_queryset.exists():
            raise ValidationError('No such cell')
        cell = cell_queryset.first()
        if amount <= 0 or amount > cell.size or amount + cell.actual_size > cell.size:
            raise ValidationError('Invalid amount provided')
        return data


class MoveProductFromCellSerializer(MoveProductSerializer):
    current_cell_id = serializers.IntegerField()

    def validate(self, data):
        amount = data.get('amount')
        new_cell_queryset = Cell.objects.filter(pk=data.get('new_cell_id'))
        current_cell_queryset = Cell.objects.filter(pk=data.get('current_cell_id'))
        if not new_cell_queryset.exists() or not current_cell_queryset.exists():
            raise ValidationError('No such cell')
        new_cell = new_cell_queryset.first()
        if amount <= 0 or amount > new_cell.size or amount + new_cell.actual_size > new_cell.size:
            raise ValidationError('Invalid amount provided')
        return data


class SendMaterialsToManufactureSerializer(serializers.Serializer):
    cell_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate(self, data):
        cell = Cell.objects.filter(pk=data.get('cell_id'))
        amount = data.get('amount')
        if not cell.exists():
            raise ValidationError('No such cell')
        if amount <= 0 or amount > cell.first().actual_size:
            raise ValidationError('Invalid amount provided')
        return data
