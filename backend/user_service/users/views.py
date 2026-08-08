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
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Logged out"})


class GetUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        user = User(email=request.user)
        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


# class UpdateUserView(GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UpdateUserSerializer

#     def get(self, request, *args, **kwargs):
#         #returns user object
#         email = self.kwargs.get("email")
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": f"User {email} does not exist"})
        
#         return Response()

#     def patch(self):

# class DeleteUserView(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = DeleteUserSerializer