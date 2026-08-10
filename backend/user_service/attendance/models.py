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
    # Define the fields for the Attendance model
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='attendances', limit_choices_to=Q(groups__name="Student"))
    timetable_entry = models.ForeignKey('entities.TimetableEntry', on_delete=models.CASCADE, related_name='attendances')
    is_present = models.BooleanField(default=False)
    datetime_in = models.DateTimeField()

    def __str__(self):
        return f"{self.timetable_entry.course.code} Attendance for - {self.user.lastname} {self.user.firstname}: {'Present' if self.is_present else 'Absent'}"
    
    def mark_attendance(self):
        self.is_present = True if self.datetime_in >= self.timetable_entry.start_datetime and self.datetime_in <= self.timetable_entry.end_datetime else False
        self.save()
        return self.is_present