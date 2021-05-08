from django.contrib.auth import login, logout
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import UserCreateSerializer
from profiles.user import User


class UserRegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class UserCheckAPIView(GenericAPIView):
    serializer_class = UserCreateSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)


class UserLogOutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response()


class UserLogInAPIView(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request, *args, **kwargs):
        login(request, request.user)
        return Response()
