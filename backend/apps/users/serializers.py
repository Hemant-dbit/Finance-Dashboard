from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ["id", "email", "username", "role", "is_active", "created_at"]
        read_only_fields = fields  # All fields are read-only here


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model  = User
        fields = ["email", "username", "password", "role"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ["role", "is_active"]
