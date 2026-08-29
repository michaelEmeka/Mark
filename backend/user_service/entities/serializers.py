from rest_framework import serializers
from .models import TimetableEntrySchedule

class GetTimetableEntryScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="timetable_entry.course.name", read_only=True)
    course_code = serializers.CharField(source="timetable_entry.course.code", read_only=True)
    lecturer_name = serializers.CharField(source="lecturer.firstname", read_only=True)
    lecture_hall = serializers.CharField(source="hall.name", read_only=True)

    class Meta:
        model = TimetableEntrySchedule
        fields = [
            "course_name",
            "course_code",
            "date",
            "lecturer_name",
            "lecture_hall",
            "attendance_taken"
        ]