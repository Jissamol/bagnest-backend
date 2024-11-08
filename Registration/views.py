from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            try:
                # Save the user and return success response
                user = serializer.save()
                return Response({
                    "user_id": user.id,
                    "username": user.username,
                    "message": "Registration successful"
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return validation errors if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
