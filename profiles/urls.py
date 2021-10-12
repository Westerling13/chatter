from django.urls import path

from profiles.views import ProfileDetailApiView

app_name = 'profile'

urlpatterns = [
    path('', ProfileDetailApiView.as_view(), name='detail'),
]
