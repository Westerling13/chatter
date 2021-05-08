"""project_root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from profiles.views import UserCheckAPIView, UserLogOutAPIView, UserLogInAPIView, UserRegisterAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', UserRegisterAPIView.as_view(), name='user_create'),
    path('api/v1/users/me/', UserCheckAPIView.as_view(), name='me'),
    path('api/v1/login/', UserLogInAPIView.as_view(), name='login'),
    path('api/v1/logout/', UserLogOutAPIView.as_view(), name='logout'),
    path('api/v1/chats/', include('chat.urls')),
]
