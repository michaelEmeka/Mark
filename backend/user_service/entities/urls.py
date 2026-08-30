from django.urls import path
from . import views

urlpatterns = [
    path("timetable/schedules/", views.GetTimetableEntryScheduleView.as_view(), name="timetable_schedules"),
    path("timetable/create_schedule/", views.CreateTimetableEntryScheduleView.as_view(), name="create_schedule"),
    path("timetable/entries/", views.GetTimetableEntriesView.as_view(), name="timetable_entries"),
]