from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.permissions import IsAdmin
from .models import User
from .serializers import UserSerializer, RegisterSerializer, UpdateRoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "register":
            return []  
        return [IsAdmin()]  

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterSerializer
        if self.action == "update_role":
            return UpdateRoleSerializer
        return UserSerializer

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        """POST /api/v1/users/register/ — public endpoint."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="role")
    def update_role(self, request, pk=None):
        """PATCH /api/v1/users/{id}/role/ — admin only."""
        user = self.get_object()
        serializer = UpdateRoleSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(user).data)
