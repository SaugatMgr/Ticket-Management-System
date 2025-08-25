from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

from apps.users.api.v1.serializers.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenVerifySerializer,
    UserListSerializer,
    UserRegisterSerializer,
)
from apps.users.models import CustomUser
from utils.services import get_instance_by_attr


class UserRegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_register_serializer = UserRegisterSerializer(data=request.data)
        user_register_serializer.is_valid(raise_exception=True)
        validated_data = user_register_serializer.validated_data

        password = validated_data.pop("password1")
        validated_data.pop("password2")
        validated_data["password"] = password

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return Response({"message": "Registration successful."})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        token_serializer = self.get_serializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        validated_data = token_serializer.validated_data
        response = {
            "token": validated_data,
            "user": UserListSerializer(validated_data.pop("user")).data,
        }
        return Response(response)


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            token_verify_serializer = self.get_serializer(data=data)
            token_verify_serializer.is_valid(raise_exception=True)
            decoded_token = AccessToken(token=data["token"])
            user = CustomUser.objects.get(id=decoded_token.payload["user_id"])
            refresh_token = RefreshToken.for_user(user)
            response = {
                "token": {
                    "access": str(decoded_token),
                    "refresh": str(refresh_token),
                    "access_expires_on": api_settings.ACCESS_TOKEN_LIFETIME,
                    "refresh_expires_on": api_settings.REFRESH_TOKEN_LIFETIME,
                },
                "user": UserListSerializer(user).data,
            }
            return Response(response)
        except Exception as e:
            return Response(
                {"error": str(e), "field": "access"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class AssignPermissionToUserView(APIView):

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        permission_ids = request.data.get("permissions")

        user = get_instance_by_attr(CustomUser, "id", user_id)
        user_role = user.role
        for permission_id in permission_ids:
            permission = get_instance_by_attr(Permission, "id", permission_id)
            if permission not in user_role.permissions.all():
                user_role.permissions.add(permission)
        return Response({"message": "Permissions assigned successfully."})
