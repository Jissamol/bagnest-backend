from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from .filters import UserFilter
from .models import User
from .serializers import UserSerializer, UserBasicDataSerializer, UserRegistrationSerializer, LoginSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, Product
from .serializers import CartSerializer

from rest_framework.permissions import IsAuthenticated

from src.accounts.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Category
from rest_framework.exceptions import ValidationError
from .serializers import ProductSerializer
from rest_framework import viewsets


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = None

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = UserFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @action(detail=False, methods=['POST'])
    #

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        data = serializer.validated_data
        email = data.get('email')  # Use email instead of username
        password = data.get('password')

        if not email or not password:
            return Response(
                {"error": "Must include email and password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate using email and password
        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {"error": "User does not exist or incorrect password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Determine role based on is_superuser
        role = "admin" if user.is_superuser else "customer"

        auth_data = {
            "token": access_token,
            "user": UserSerializer(instance=user, context={'request': request}).data,
            "role": role
        }

        return Response(
            {"message": "Login successful", "data": auth_data},
            status=status.HTTP_200_OK
        )

    # @action(detail=False, methods=['POST'])
    # def logout(self, request):
    #     if request.user.is_authenticated:
    #         Token.objects.filter(user=request.user).delete()
    #         logout(request)
    #     return Response(
    #         {"message": "Successfully logged out."},
    #         status=status.HTTP_200_OK)
    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()  # Delete the token
            logout(request)
        return Response(
            {"message": "Successfully logged out."},
            status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        data = serializer.validated_data

        user = User.objects.create(**dict(data), is_active=True)
        user_obj = User.objects.filter(email=data.get('email')).first()
        if user_obj:
            user_obj.set_password(data.get('password'))
            user_obj.save()
        data = UserRegistrationSerializer(user).data
        return Response(
            {"message": "Created", "data": data},
            status=status.HTTP_201_CREATED
        )

    @action(methods=['GET'], detail=False, pagination_class=StandardResultsSetPagination)
    def users_list(self, request):
        queryset = User.objects.all()
        self.filterset_class = UserFilter
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(UserBasicDataSerializer(page, many=True).data)
        return Response(
            {"message": "Successfully fetched", "data": UserBasicDataSerializer(queryset, many=True).data},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'])
    def password_change(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        data = serializer.validated_data

        user = request.user
        new_password = data.get('new_password')

        if new_password:
            if len(new_password) < 6:
                return Response(
                    {"error": 'Password too short.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if not user.check_password(data.get('old_password')):
            return Response(
                {"error": 'Old password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['POST'])
    def categories(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        category = serializer.save()  # Automatically saves image if provided
        data = CategorySerializer(category).data
        return Response(
            {"message": "Category created successfully", "data": data},
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        # Fetch and paginate categories
        queryset = Category.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(CategorySerializer(page, many=True).data)

        # If no pagination, return all categories
        return Response(
            {"message": "Successfully fetched", "data": CategorySerializer(queryset, many=True).data},
            status=status.HTTP_200_OK
        )


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')  # Retrieve category_id from URL parameters

        # If category_id is provided, filter products by category
        if category_id:
            return Product.objects.filter(category_id=category_id)  # Filter products by category_id

        return Product.objects.all()  # Return all products if no category_id is specified

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Get filtered queryset by category_id
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(ProductSerializer(page, many=True).data)

        return Response(
            {"message": "Successfully fetched", "data": ProductSerializer(queryset, many=True).data},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'])
    def product(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            product = serializer.save()
            data = ProductSerializer(product).data
            return Response(
                {"message": "Product created successfully", "data": data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def cart(self, request):
        try:
            serializer = CartSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            cart = serializer.save()
            data = CartSerializer(cart).data
            return Response(
                {"message": "cart created successfully", "data": data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

