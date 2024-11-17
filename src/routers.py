from rest_framework import routers
from django.urls import path, include

from .accounts.viewsets import UserViewSet

router = routers.DefaultRouter()

# user
router.register(r'users', UserViewSet, basename='auth')


urlpatterns = [
    path('api/', include(router.urls)),
]
