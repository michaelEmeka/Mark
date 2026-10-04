from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/user/", include('users.urls')),
    path("api/v1/entities/", include('entities.urls')),
    path("api/v1/attendance/", include('attendance.urls'))
]
