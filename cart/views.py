from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .pagination import CustomPagination


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # Generate JWT tokens
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    authentication_classes = [JWTAuthentication]  # Explicitly setting JWT Authentication
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.all()
        paginator = CustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)  # Apply pagination
        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
