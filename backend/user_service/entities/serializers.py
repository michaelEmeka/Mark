from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import TimetableEntrySchedule, TimetableEntry, Course, Timetable

class GetTimetableEntryScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="timetable_entry.course.name", read_only=True)
    course_code = serializers.CharField(source="timetable_entry.course.code", read_only=True)
    lecturer_name = serializers.CharField(source="lecturer.firstname", read_only=True)
    lecture_hall = serializers.CharField(source="hall.name", read_only=True)

    class Meta:
        model = TimetableEntrySchedule
        fields = [
            "id",
            "course_name",
            "course_code",
            "date",
            "lecturer_name",
            "lecture_hall",
            "attendance_taken"
        ]

class GetTimetableEntriesSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)
    semester_name = serializers.CharField(source="timetable.semester.name", read_only=True)
        
    class Meta:
        model = TimetableEntry
        fields = [
            "id",
            "course_name",
            "course_code",
            "semester_name",
            "day",
            "start_time",
            "end_time",
            "timetable",
            "is_one_time"
        ]

# class CreateTimetableEntryScheduleSerializer(serializers.ModelSerializer):
#     timetable_entry_id = serializers.IntegerField()

#     #new timetableentry optional fields
#     course_id = serializers.IntegerField(required=False, allow_null=True)
#     start_time = serializers.TimeField(required=False, allow_null=True)
#     end_time = serializers.TimeField(required=False, allow_null=True)

#     #date = models.DateField()
#     #lecturer = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="timetable_entries", limit_choices_to=Q(groups__name="Lecturer"))
#     #hall = models.ForeignKey("entities.Hall", on_delete=models.CASCADE)
    
#     class Meta:
#         model = TimetableEntrySchedule
#         fields = [
#             "timetable_entry_id",
#             "course_id",
#             "start_time",
#             "end_time",
#             "date",
#             "lecturer",
#             "hall"
#         ]
    
#     def create(self, validated_data):
#         timetable_entry_id = validated_data.pop("timetable_entry_id")
#         try:
#             timetable_entry, created = TimetableEntry.objects.get_or_create(id=timetable_entry_id, defaults={"is_one_time": True})
#             if created:
#                 course_id = validated_data.pop("course_id")
#                 start_time = validated_data.pop("start_time")
#                 end_time = validated_data.pop("end_time")
#                 department = self.context.get("department")
#                 level = self.context.get("level")

#                 if not (course_id and start_time and end_time):
#                     raise Exception("course, start_time and end_time fields are required")
#                 if start_time > end_time:
#                     raise Exception("start_time is later than end_time")
#                 try:
#                     course = Course.objects.get(id=course_id, department=department, level=level)
#                 except Course.DoesNotExist:
#                     raise Exception("selected course does not exist for this user")
#                 timetable_entry.course = course
#                 timetable_entry.start_time = start_time
#                 timetable_entry.end_time = end_time
#                 timetable_entry.is_one_time = True
#                 timetable_entry.save()
#             timetable_entry_schedule = TimetableEntrySchedule.objects.create(timetable_entry=timetable_entry, **validated_data)
#         except:
#             if created:
#                 raise Exception("Could not create Timetable Schedule, but successfully created new timetable entry")
#             raise Exception("Could not create Timetable Schedule")

#         return timetable_entry_schedule


class CreateTimetableEntryScheduleSerializer(serializers.ModelSerializer):
    timetable_entry_id = serializers.IntegerField(required=True, allow_null=True)
    # Used when timetable_entry_id doesn't identify an existing entry
    course_id = serializers.IntegerField(required=True, allow_null=True)
    start_time = serializers.TimeField(required=True, allow_null=True)
    end_time = serializers.TimeField(required=True, allow_null=True)

    class Meta:
        model = TimetableEntrySchedule
        fields = [
            "timetable_entry_id",
            "course_id",
            "start_time",
            "end_time",
            "date",
            "lecturer",
            "hall",
        ]

    @transaction.atomic
    def create(self, validated_data):
        timetable_entry_id = validated_data.pop("timetable_entry_id")

        department = self.context["department"]
        level = self.context["level"]

        # Try to find an EXISTING timetable entry belonging
        # to this user's department + level.
        try:
            timetable_entry = TimetableEntry.objects.get(
                id=timetable_entry_id,
                timetable__department=department,
                timetable__level=level,
                course__department=department,
                course__level=level,
            ) #use current timetable instead to obt, ain timetableentry later, cause the current timetable
            #might not have courses that satisfy the current filter(due to probably they're old courses).
            #so user can only create schedule for courses(timetableentry) in their timetable
            validated_data.pop("course_id", None)
            validated_data.pop("start_time", None)
            validated_data.pop("end_time", None)

        except TimetableEntry.DoesNotExist:
            course_id = validated_data.pop("course_id", None)
            start_time = validated_data.pop("start_time", None)
            end_time = validated_data.pop("end_time", None)

            if course_id is None:
                raise serializers.ValidationError({"course_id": "This field is required for an impromptu class."})

            if start_time is None:
                raise serializers.ValidationError({"start_time": "This field is required for an impromptu class."})

            if end_time is None:
                raise serializers.ValidationError({"end_time": "This field is required for an impromptu class."})

            if start_time >= end_time:
                raise serializers.ValidationError({"start_time": "start_time must be earlier than end_time."})

            try:
                course = Course.objects.get(
                    id=course_id,
                    department=department,
                    level=level
                )
            except Course.DoesNotExist:
                raise serializers.ValidationError({
                    "course_id": "Selected course does not exist for this user."
                })

            timetable = Timetable.objects.filter(
                        department=department,
                        level=level
                    ).order_by("-created_at").first()
            if timetable is None:
                raise serializers.ValidationError(
                    "No timetable exists for this department and level."
                )
            
            timetable_entry = TimetableEntry.objects.create(
                course=course,
                timetable=timetable,
                start_time=start_time,
                end_time=end_time,
                is_one_time=True
            )
        
        #Later we want to verify the lecturer is a lecturer not a student user, and also he belongs in the department
        return TimetableEntrySchedule.objects.create(
            timetable_entry=timetable_entry,
            **validated_data
        )