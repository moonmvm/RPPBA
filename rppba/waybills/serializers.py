from rest_framework import serializers

from .models import Clientele, Waybill


class ClienteleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientele
        fields = '__all__'


class WaybillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waybill
        fields = '__all__'


class WaybillReadOnlySerializer(WaybillSerializer):
    firm_participant = ClienteleSerializer()
    clientele_participant = ClienteleSerializer()
