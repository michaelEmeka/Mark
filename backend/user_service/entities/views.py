from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
#from .serializers import UserSerializer
from .models import *
from users.models import User
from .serializers import *

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
            many=True
        )

        return Response({"Scheduled": serializer.data})