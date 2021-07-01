from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from profiles.views import UserCheckAPIView, UserLogOutAPIView, UserLogInAPIView, UserRegisterAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/users/', UserRegisterAPIView.as_view(), name='user_register'),
    path('api/v1/users/me/', UserCheckAPIView.as_view(), name='me'),
    path('api/v1/login/', UserLogInAPIView.as_view(), name='login'),
    path('api/v1/logout/', UserLogOutAPIView.as_view(), name='logout'),
    path('api/v1/chats/', include('chat.urls')),
]
