from django.contrib import admin

from users.models import User
from entities.models import *

admin.site.register(User)
admin.site.register(University)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Level)
admin.site.register(Set)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(Hall)
admin.site.register(Timetable)
admin.site.register(TimetableEntry)
admin.site.register(TimetableEntrySchedule)