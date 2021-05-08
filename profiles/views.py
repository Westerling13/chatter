from django.contrib.auth import login, authenticate, logout
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import UserSerializer, UserLogInSerializer
from profiles.user import User


class UserRegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class UserCheckAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)


class UserLogOutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response()


class UserLogInAPIView(GenericAPIView):
    permission_classes = [~IsAuthenticated]
    serializer_class = UserLogInSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request, username=serializer.validated_data['username'], password=serializer.validated_data['password'],
        )
        if user is None:
            raise ValidationError('Invalid login')

        login(request, user)

        return Response()
