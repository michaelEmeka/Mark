from django.contrib import admin

from .models import Attendance, FingerprintStamp, HardwareNode

# Register your models here.
admin.site.register(Attendance)
admin.site.register(HardwareNode)
admin.site.register(FingerprintStamp)