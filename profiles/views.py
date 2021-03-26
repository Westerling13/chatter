from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from profiles.serializers import UserSerializer
from profiles.user import User


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects

