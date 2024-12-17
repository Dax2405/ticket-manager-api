from rest_framework import serializers
from .models import Enterprise, Ticket, In_Place, Place, Logs


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    destination_name = serializers.SerializerMethodField()
    enterprise_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_destination_name(self, obj):
        return obj.destination.name

    def get_enterprise_name(self, obj):
        return obj.enterprise.name

    def validate_id_number(self, value):
        if Ticket.objects.filter(id_number=value).exists():
            raise serializers.ValidationError(
                "A ticket with this ID number already exists.")
        return value


class InPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = In_Place
        fields = '__all__'


class LogsSerializer(serializers.ModelSerializer):
    ticket_name = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()

    class Meta:
        model = Logs
        fields = ['id', 'ticket', 'place', 'action',
                  'time', 'ticket_name', 'place_name']

    def get_ticket_name(self, obj):
        return obj.ticket.name

    def get_place_name(self, obj):
        return obj.place.name
