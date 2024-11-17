from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import UserFilter
from .models import User
from .serializers import UserSerializer, UserBasicDataSerializer, UserRegistrationSerializer, LoginSerializer


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
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        data = serializer.validated_data

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return Response(
                {"error": 'Must Include username and password.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=username).first()
        if not user:
            return Response(
                {"error": 'User does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            auth_data = {
                "token": token.key,
                "user": UserSerializer(instance=user, context={'request': request}).data
            }
            return Response(
                {"message": "Success", "data": auth_data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": 'Incorrect Email and Password.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
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
        return response.Ok(content)
