from django.urls import path

from . import views

urlpatterns = [
    path("universities/", views.GetUniversitiesView.as_view(), name="get_universities"),
    path("schools/", views.GetSchoolsView.as_view(), name="get_schools"),
    path("departments/", views.GetDepartmentsView.as_view(), name="get_departments"),
    path("sets/", views.GetSetsView.as_view(), name="get_sets"),
    path("levels/", views.GetLevelsView.as_view(), name="get_levels"),
    path("timetable/schedules/", views.GetTimetableEntryScheduleView.as_view(), name="timetable_schedules"),
    path("timetable/create_schedule/", views.CreateTimetableEntryScheduleView.as_view(), name="create_schedule"),
    path("timetable/entries/", views.GetTimetableEntriesView.as_view(), name="timetable_entries"),
]