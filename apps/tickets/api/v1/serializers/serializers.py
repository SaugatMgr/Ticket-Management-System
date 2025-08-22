from rest_framework import serializers

from apps.tickets.models import Ticket, TicketPriority, TicketStatus


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "assigned_to",
            "menu",
            "status",
            "priority",
        ]


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = [
            "id",
            "name",
            "description",
        ]


class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = [
            "id",
            "name",
            "description",
        ]
