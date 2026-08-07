from django.contrib import admin

from users.models import User
from entities.models import University, School, Department

admin.site.register(User)
admin.site.register(University)
admin.site.register(School)
admin.site.register(Department)
# Register your models here.
