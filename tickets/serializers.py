from rest_framework import serializers
from .models import Enterprise, Ticket, In_Place, Place


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class InPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = In_Place
        fields = '__all__'
