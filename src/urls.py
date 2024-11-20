from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.accounts.viewsets import UserViewSet, CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('api/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('api/product/', ProductViewSet.as_view({'post': 'create'}), name='product-create'),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
