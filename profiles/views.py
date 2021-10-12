from django.contrib.auth import login
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from profiles.serializers import UserCreateSerializer, ProfileSerializer
from profiles.user import User


class UserRegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects

    def post(self, request, *args, **kwargs):
        """Регистрация пользователя."""
        if request.user.is_authenticated:
            raise PermissionDenied
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class ProfileDetailApiView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        """Информация о профиле."""
        return self.retrieve(request, *args, **kwargs)
