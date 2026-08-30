from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
#from .serializers import UserSerializer
from .models import *
from users.models import User
from .serializers import *
from rest_framework import status

class GetUniversitiesView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetSchoolsView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetDepartmentsView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetSets(ListAPIView):
    queryset = University.objects.all()
    pass

class GetLevelsView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetSessionsView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetSemestersView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetCoursesView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetTimetableView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetTimetableEntryView(ListAPIView):
    queryset = University.objects.all()
    pass

class GetTimetableEntryScheduleView(GenericAPIView):
    serializer_class = GetTimetableEntryScheduleSerializer

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        active_timetable_entries_schedules = (
            TimetableEntrySchedule.objects.filter(
                    timetable_entry__timetable=user.set.timetable
                )
            )
        print(active_timetable_entries_schedules)
        serializer = self.get_serializer(
            active_timetable_entries_schedules,
            many=True, context={"department": request.user.department, "level": request.user.level}
        )

        return Response({"TimetableEntries Schedules": serializer.data}, status=status.HTTP_200_OK)

class GetTimetableEntriesView(GenericAPIView):
    serializer_class = GetTimetableEntriesSerializer
    def get(self, request):
        user = User.objects.get(email=request.user.email)
        timetable_entries = TimetableEntry.objects.filter(timetable=user.set.timetable)
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