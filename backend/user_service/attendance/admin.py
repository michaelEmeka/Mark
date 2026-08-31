from django.contrib import admin
from .models import HardwareNode, Attendance, FingerprintStamp
# Register your models here.
admin.site.register(Attendance)
admin.site.register(HardwareNode)
admin.site.register(FingerprintStamp)