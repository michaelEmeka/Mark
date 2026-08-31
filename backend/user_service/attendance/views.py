from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from entities.models import TimetableEntrySchedule
from .serializers import ListUserAttendanceSerilaizer
from .models import Attendance

class ListUserAttendance(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListUserAttendanceSerilaizer

    def get_queryset(self):
        return Attendance.objects.filter(user=self.request.user)

class CreateAttendance(APIView):

    def post(self, request):
        user = request.user
        now = timezone.localtime()
        today = now.date()
        current_time = now.time()
        department = user.department
        level = user.level

        # Find a class currently taking place for this student's
        # department and level.
        schedule = (
            TimetableEntrySchedule.objects
            .filter(
                date=today,
                timetable_entry__timetable__department=department,
                timetable_entry__timetable__level=level,
                timetable_entry__start_time__lte=current_time,
                timetable_entry__end_time__gte=current_time,
            )
            .select_related("timetable_entry")
            .first()
        )

        if schedule is None:
            raise ValidationError(
                "There is no scheduled class at this time."
            )

        # Prevent the student from checking into the same class twice.
        if Attendance.objects.filter(
            user=user,
            timetable_entry_schedule=schedule,
        ).exists():
            raise ValidationError(
                "You have already checked in for this class."
            )

        attendance = Attendance.objects.create(
            user=user,
            timetable_entry_schedule=schedule,
            time_in=current_time,
            is_present=True,
        )

        return Response(
            {
                "message": "Attendance recorded successfully.",
                "is_present": attendance.is_present,
                "course": schedule.timetable_entry.course.code,
                "time_in": attendance.time_in,
            },
            status=status.HTTP_201_CREATED,
        )