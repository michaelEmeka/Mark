from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *



class ListUsersView(ListAPIView):
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
        return Response(serializer.errors)

class LoginUserView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get("email"))
            password = request.data.get("password")
            if user.check_password(password):
                tokens = user.tokens()
                return Response(
                    tokens, status=status.HTTP_200_OK
                )
            else:
                return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "Signup to create an account"})


class LogoutUserView(APIView):
    def post(self, request):
        refresh = request.data.get("refresh")
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception as e:
            raise e
        return Response({"message": "Logged out"})


class GetUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, context={"user": request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message": f"User {user.email} updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": f"Could not update User {instance.email}.."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# class DeleteUserView(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = DeleteUserSerializer