from django.urls import path
from . import views

urlpatterns = [
    path("user/timetable_schedules/", views.GetTimetableEntryScheduleView.as_view(), name="timetable_schedules")
]