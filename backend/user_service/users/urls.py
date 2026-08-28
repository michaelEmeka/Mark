from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("", views.GetUserView.as_view(), name="get_user"),
    path('students/', views.ListUsersView.as_view(), name="get_users"),
    path("signup/", views.CreateUserView.as_view(), name="signup_user"),
    path("login/", views.LoginUserView.as_view(), name="login_user"),
    path("logout/", views.LogoutUserView.as_view(), name="logout_user"),
    path("update/", views.UpdateUserView.as_view(), name="update_user"),
    path("token/refresh/", TokenRefreshView.as_view(), name='refresh_user_token')
]