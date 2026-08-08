from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.ListUsersView.as_view()),
    path("signup/", views.CreateUserView.as_view()),
    path("login/", views.LoginUserView.as_view()),
    path("logout/", views.LogoutUserView.as_view()),
    path("", views.GetUserView.as_view())
    #path("get_user/<int:pk>", views.GetUserView.as_view())
]
