from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from users.models import User

#from .serializers import UserSerializer
from .models import *
from .serializers import *


def resolve_user_set(user):
    if not user:
        return None

    if (user.set_id and
            user.set.department_id == user.department_id
            and user.set.department.school_id == user.school_id
            and user.set.department.school.university_id == user.university_id
        ):
            return user.set

    return (
        Set.objects.filter(
            department__school__university_id=user.university_id,
            department__school_id=user.school_id,
            department_id=user.department_id,
        )
        .order_by("-start_year", "-end_year")
        .first()
    )


class GetUniversitiesView(ListAPIView):
    queryset = University.objects.all()
    serializer_class = GetUniversitiesSerializer

#-----------------------------
class GetSchoolsView(ListAPIView):
    serializer_class = GetSchoolsSerializer

    def get_queryset(self):
        university_id = self.request.query_params.get("university")
        if university_id:
            return School.objects.filter(university_id=university_id).order_by("name")
        return School.objects.all().order_by("name")


class GetDepartmentsView(ListAPIView):
    serializer_class = GetDepartmentsSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get("school")
        university_id = self.request.query_params.get("university")

        queryset = Department.objects.select_related("school", "school__university")

        if school_id:
            return queryset.filter(school_id=school_id).order_by("name")

        if university_id:
            return queryset.filter(school__university_id=university_id).order_by("name")

        return queryset.order_by("name")

class GetSetsView(ListAPIView):
    serializer_class = GetSetsSerializer

    def get_queryset(self):
        queryset = Set.objects.select_related("department", "department__school", "department__school__university")
        department_id = self.request.query_params.get("department")
        school_id = self.request.query_params.get("school")
        university_id = self.request.query_params.get("university")

        if department_id:
            return queryset.filter(department_id=department_id).order_by("-start_year", "-end_year")
        if school_id:
            return queryset.filter(department__school_id=school_id).order_by("department__name", "-start_year", "-end_year")
        if university_id:
            return queryset.filter(department__school__university_id=university_id).order_by("department__name", "-start_year", "-end_year")

        return queryset.order_by("department__name", "-start_year", "-end_year")

class GetLevelsView(ListAPIView):
    serializer_class = GetLevelsSerializer
    queryset = Level.objects.all().order_by("code")

class GetSessionsView(ListAPIView):
    queryset = University.objects.all()

class GetSemestersView(ListAPIView):
    queryset = University.objects.all()

class GetCoursesView(ListAPIView):
    queryset = University.objects.all()

class GetTimetableView(ListAPIView):
    queryset = University.objects.all()

class GetTimetableEntryView(ListAPIView):
    queryset = University.objects.all()

class GetTimetableEntryScheduleView(GenericAPIView):
    serializer_class = GetTimetableEntryScheduleSerializer

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        current_set = resolve_user_set(user)

        active_timetable_entries_schedules = (
            TimetableEntrySchedule.objects.filter(
                timetable_entry__timetable__set=current_set
            )
            if current_set
            else TimetableEntrySchedule.objects.none()
        )

        serializer = self.get_serializer(
            active_timetable_entries_schedules,
            many=True,
            context={"department": request.user.department, "level": request.user.level},
        )

        return Response({"TimetableEntries Schedules": serializer.data}, status=status.HTTP_200_OK)

class GetTimetableEntriesView(GenericAPIView):
    serializer_class = GetTimetableEntriesSerializer

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        current_set = resolve_user_set(user)
        timetable_entries = (
            TimetableEntry.objects.filter(timetable__set=current_set)
            if current_set
            else TimetableEntry.objects.none()
        )
        serializer = self.get_serializer(timetable_entries, many=True)

        return Response({"TimetableEntries": serializer.data}, status=status.HTTP_200_OK)

class CreateTimetableEntryScheduleView(GenericAPIView):
    queryset = TimetableEntrySchedule.objects.all()
    serializer_class = CreateTimetableEntryScheduleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["department"] = self.request.user.department
        context["level"] = self.request.user.level
        return context

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            "Schedule created Successfully!",
            status=status.HTTP_201_CREATED
        )