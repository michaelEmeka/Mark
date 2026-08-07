from django.contrib import admin

from users.models import User
from entities.models import University, School, Department, Level, Course, Semester, Hall, TimeTable, TimetableEntry

admin.site.register(User)
admin.site.register(University)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Level)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Hall)
admin.site.register(TimeTable)
admin.site.register(TimetableEntry)
