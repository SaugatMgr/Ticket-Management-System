from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.settings import api_settings

from apps.users.models import CustomUser, Permission, Role
from utils.services import generate_error


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
        write_only_fields = (
            "password1",
            "password2",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise serializers.ValidationError(generate_error("Passwords do not match."))
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "username",
            "email",
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = self.user
        data["access_expires_on"] = api_settings.ACCESS_TOKEN_LIFETIME
        data["refresh_expires_on"] = api_settings.REFRESH_TOKEN_LIFETIME

        return data


class CustomTokenVerifySerializer(TokenVerifySerializer):
    token = serializers.CharField(max_length=500, required=True)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "codename", "description"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]


class CreateRoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True
    )

    class Meta:
        model = Role
        fields = ["name", "permissions"]
