import django_filters

from .models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'mobile': ['icontains'],
            'email': ['icontains'],
            'address': ['icontains'],
            'is_staff': ['exact'],
            'is_superuser': ['exact'],
        }
