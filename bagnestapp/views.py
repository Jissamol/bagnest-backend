# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserSerializer, LoginSerializer


# Register User View
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user_id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login User View for Token-based authentication
class LoginUser(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # Assuming your LoginSerializer returns a validated user
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Custom Login View for Browser-based Authentication
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect superuser to admin home page
            if user.is_superuser:
                return redirect('/admin-home/')  # URL for admin home
            else:
                return redirect('/home/')  # URL for regular user home
        else:
            return HttpResponse("Invalid login credentials")
    return HttpResponse("Login page")


# Admin Home Page
@login_required
def admin_home_page(request):
    if request.user.is_superuser:
        return render(request, 'admin_home.html')
    else:
        return HttpResponse("Unauthorized", status=401)
