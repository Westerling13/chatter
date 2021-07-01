from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from profiles.views import UserCheckAPIView, UserRegisterAPIView
from project_root.swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/users/', UserRegisterAPIView.as_view(), name='user_register'),
    path('api/v1/users/me/', UserCheckAPIView.as_view(), name='me'),
    path('api/v1/chats/', include('chat.urls')),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
