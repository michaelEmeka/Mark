from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from .serializers import *


class ListUsersView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer

    def get(self):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateUserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):  
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": f"User {user.email} created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Signup to create an account"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            tokens = user.tokens()
            return Response(tokens, status=status.HTTP_200_OK)

        if user.password == password:
            user.set_password(password)
            user.save(update_fields=["password"])
            tokens = user.tokens()
            return Response(tokens, status=status.HTTP_200_OK)

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh = request.data.get("refresh")
        token = RefreshToken(refresh)
        token.blacklist()
        
        return Response({"message": "Logged out"})


class GetUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    def patch(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
            context={"user": request.user},
        )
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message": f"User {user.email} updated successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Could not update user."}, status=status.HTTP_400_BAD_REQUEST)
# class DeleteUserView(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = DeleteUserSerializer