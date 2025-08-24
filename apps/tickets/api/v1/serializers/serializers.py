from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.tickets.models import (
    MenuLevel1,
    MenuLevel2,
    MenuLevel3,
    Ticket,
    TicketPriority,
    TicketStatus,
)
from apps.users.api.v1.serializers.serializers import RoleSerializer

User = get_user_model()


class MenuLevel1Serializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLevel1
        fields = ["id", "name"]


class MenuLevel2ListDetailSerializer(serializers.ModelSerializer):
    parent = MenuLevel1Serializer(read_only=True)

    class Meta:
        model = MenuLevel2
        fields = ["id", "parent", "name"]


class MenuLevel2CreateUpdateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MenuLevel1.objects.all(),
    )

    class Meta:
        model = MenuLevel2
        fields = ["id", "parent", "name"]


class MenuLevel3ListDetailSerializer(serializers.ModelSerializer):
    parent = MenuLevel2ListDetailSerializer(read_only=True)

    class Meta:
        model = MenuLevel3
        fields = ["id", "parent", "name"]


class MenuLevel3CreateUpdateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MenuLevel2.objects.all(),
    )

    class Meta:
        model = MenuLevel3
        fields = ["id", "parent", "name"]


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = [
            "id",
            "name",
            "weight",
        ]


class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = [
            "id",
            "name",
            "weight",
        ]


class TicketListSerializer(serializers.ModelSerializer):
    class TicketUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "full_name",
            ]

    class TicketMenuLevel3Serializer(serializers.ModelSerializer):
        class Meta:
            model = MenuLevel3
            fields = [
                "id",
                "name",
            ]

    created_by = TicketUserSerializer(read_only=True)
    assigned_to = TicketUserSerializer(read_only=True)
    menu = TicketMenuLevel3Serializer(read_only=True)
    status = TicketStatusSerializer(read_only=True)
    priority = TicketPrioritySerializer(read_only=True)

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


class TicketDetailSerializer(serializers.ModelSerializer):
    class TicketUserSerializer(serializers.ModelSerializer):
        role = RoleSerializer(read_only=True)
        full_name = serializers.CharField(source="get_full_name", read_only=True)

        class Meta:
            model = User
            fields = [
                "id",
                "full_name",
                "role",
            ]

    created_by = TicketUserSerializer(read_only=True)
    assigned_to = TicketUserSerializer(read_only=True)
    menu = MenuLevel3ListDetailSerializer(read_only=True)
    status = TicketStatusSerializer(read_only=True)
    priority = TicketPrioritySerializer(read_only=True)

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


class TicketCreateUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    menu = serializers.PrimaryKeyRelatedField(queryset=MenuLevel3.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=TicketStatus.objects.all())

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
