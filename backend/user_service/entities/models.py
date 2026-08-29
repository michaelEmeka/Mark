from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class University(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __str__(self):
            return self.name

class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    address = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='schools')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class Set(models.Model):
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sets')
    timetable = models.OneToOneField("entities.Timetable", on_delete=models.CASCADE, related_name="set", null=True, blank=True)

    def __str__(self):
        return f"{self.department.code} - {self.start_year}/{self.end_year}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["department", "start_year", "end_year"],
                name="unique_set_per_department"
            )
        ]

class Level(models.Model):
    code = models.PositiveIntegerField(
        validators=[
        MinValueValidator(100),
        MaxValueValidator(600),
    ], unique=True)

    def __str__(self):
        return str(self.code) + " Level"

#Curriculum Models
class Session(models.Model):
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.start_year}/{self.end_year}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["start_year", "end_year"],
                name="unique_session"
            )
        ]
    
class Semester(models.Model):
    SEMESTER_CHOICES = [
        ("Harmattan", "Harmattan Semester"),
        ("Rain", "Rain Semester"),
    ]
    name = models.CharField(max_length=30, choices=SEMESTER_CHOICES )  # First Semester
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.session} - {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "name"],
                name="unique_semester_per_session"
            )
        ]

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ManyToManyField(
        Department,
        related_name="courses"
    )
    level = models.ManyToManyField(Level, related_name="courses")
    units = models.PositiveIntegerField(default=3)
    lecturer = models.ManyToManyField("users.User", related_name="courses", blank=True, limit_choices_to=Q(groups__name="Lecturer"))

    def __str__(self):
        return f"{self.code} - {self.name}"

class Timetable(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="timetables"
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department.name} | {self.level.__str__()} | {self.semester.name}"

class TimetableEntry(models.Model):
    """
    TimetableEntry model. This represents a single entry on the timetable

    is_one_time: indicates if the timetableentry is temporary. It is relevant to generate
    timetableentryschedule for imporomptu class. If true it doesn't show up as timetableentry
    in user dashboard
    """
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="timetable_entries")
    day = models.CharField(max_length=3, choices=DAYS, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name="timetable_entries")
    is_one_time = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.code} | {self.day} | ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = "Timetable Entry"
        verbose_name_plural = "Timetable Entries"
        constraints = [
                        models.UniqueConstraint(
                            fields=[
                                "timetable",
                                "course",
                                "day",
                                "start_time",
                                "end_time",
                            ],
                            name="unique_timetable_entry",
                        ),
                    ]

class TimetableEntrySchedule(models.Model):
    timetable_entry = models.ForeignKey(TimetableEntry, on_delete=models.CASCADE, related_name="timetable_entry_schedules")
    date = models.DateField()
    lecturer = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="timetable_entries", limit_choices_to=Q(groups__name="Lecturer"))
    hall = models.ForeignKey("entities.Hall", on_delete=models.CASCADE)
    attendance_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.timetable_entry.course.code} | {self.date} | ({self.timetable_entry.start_time} - {self.timetable_entry.end_time})"

    def map_date_to_day(self):
        date_str = str(self.date)  # YYYY-MM-DD format
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day_name = date_obj.strftime("%A")  # Full day name (e.g., Friday)
        return day_name

    def is_past(self):
        return self.date < datetime.now().date()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["timetable_entry", "date"],
                name="unique_timetable_entry_schedule"
            )
        ]
            

class Hall(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='halls')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='halls', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='halls', null=True, blank=True)

    def __str__(self):
        return self.name