from rest_framework import serializers
from .models import Attendance

class ListUserAttendanceSerilaizer(serializers.ModelSerializer):
    course = serializers.JSONField(read_only=True)
    #course_name = serializers.CharField(source="timetable_entry_schedule.timetable_entry.course.name", read_only=True)
    #course_code = serializers.CharField(source="timetable_entry_schedule.timetable_entry.course.code", read_only=True)
    lecturer = serializers.CharField(source="timetable_entry_schedule.lecturer.username", read_only=True)
    timetable_entry_schedule_id = serializers.IntegerField(
    source="timetable_entry_schedule.id",
    read_only=True
)
    class Meta:
        model = Attendance
        fields = [
            "course",
            "lecturer",
            "timetable_entry_schedule_id",
            "date_taken",
            "time_in",
            "is_present"
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        course = ( instance .timetable_entry_schedule .timetable_entry .course )
        representation["course"] = {
            "code": course.code,
            "name": course.name
            }
        return representation