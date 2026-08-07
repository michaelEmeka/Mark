from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100)
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
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='schools')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=30)  # First Semester
    session = models.CharField(max_length=20)  # 2026/2027

    def __str__(self):
        return f"{self.session} - {self.name}"


class Hall(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    units = models.PositiveIntegerField(default=3)
    lecturer = models.ManyToManyField("users.User", related_name="courses", blank=True, limit_choices_to={'is_lecturer': True})

    def __str__(self):
        return f"{self.code} - {self.name}"

class TimeTable(models.Model):
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
        return f"{self.department.name} | {self.level.name} | {self.semester.name}"

class TimetableEntry(models.Model):
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="timetable_entries")
    lecturer = models.ForeignKey("users.User", on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    day = models.CharField(max_length=3, choices=DAYS)

    start_time = models.TimeField()
    end_time = models.TimeField()

    timetable = models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name="timetable_entries")

    def __str__(self):
        return f"{self.course.code} | {self.day} | ({self.start_time} - {self.end_time})"