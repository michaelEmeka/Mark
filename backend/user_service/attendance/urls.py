from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateAttendance.as_view()),
    path("", views.ListUserAttendance.as_view())
]