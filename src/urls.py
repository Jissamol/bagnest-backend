
# path('view-cart/', ViewCartView.as_view(), name='view_cart'),
# path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove_from_cart'),
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.accounts.viewsets import UserViewSet, CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('api/product/', ProductViewSet.as_view({'post': 'product'}), name='product'),
    path('api/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('api/categories/<int:category_id>/products/', ProductViewSet.as_view({'get': 'list'}), name='category-products'),
    path('api/', include(router.urls)),
    path('cart/', ProductViewSet.as_view({'post': 'cart'}), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
