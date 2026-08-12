from django.db import models
from django.db.models import Q
from entities.models import School, Department, TimetableEntry

class HardwareNode(models.Model):
    name = models.CharField(max_length=100, default="university.name-school.name-department.name-Node")
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey('entities.Department', on_delete=models.CASCADE, related_name='hardware_nodes')
    school = models.ForeignKey('entities.School', on_delete=models.CASCADE, related_name='hardware_nodes', null=True, blank=True)
    university = models.ForeignKey('entities.University', on_delete=models.CASCADE, related_name='hardware_nodes', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"
    


class Attendance(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='attendances',
        limit_choices_to=Q(groups__name="Student")
    )

    timetable_entry_schedule = models.ForeignKey(
        'entities.TimetableEntrySchedule',
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    date_taken = models.DateField(auto_now_add=True)
    time_in = models.TimeField()
    is_present = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'timetable_entry_schedule'],
                name='unique_student_attendance_per_schedule'
            )
        ]

    def __str__(self):
        status = "Present" if self.is_present else "Absent"

        return (
            f"{self.timetable_entry_schedule.timetable_entry.course.code} "
            f"Attendance for - "
            f"{self.user.lastname} {self.user.firstname}: {status}"
        )

    def mark_attendance(self):
        timetable_entry = self.timetable_entry_schedule.timetable_entry

        self.is_present = (
            timetable_entry.start_time
            <= self.time_in
            <= timetable_entry.end_time
        )

        self.save(update_fields=['is_present'])

        return self.is_present