# api/views.py
from rest_framework import viewsets, views
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Example of a function-based view (FBV)
def some_view(request):
    # Get all products
    products = Product.objects.all()
    # Return product names as a simple JSON response
    product_names = [product.name for product in products]
    return JsonResponse({'products': product_names})

# Class-Based View for listing products
class ProductList(views.APIView):
    def get(self, request):
        products = Product.objects.all()  # Query all products
        serializer = ProductSerializer(products, many=True)  # Serialize the products
        return Response(serializer.data)  # Return serialized data as response

# DRF viewsets for handling products and categories
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
