from django.contrib import admin
from .models import HardwareNode, Attendance
# Register your models here.
admin.site.register(Attendance)
admin.site.register(HardwareNode)