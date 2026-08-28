from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import UserSerializer
from .models import 


class GetUniversitiesView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetSchoolsView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetDepartmentsView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetSets(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetLevelsView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetSessionsView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetSemestersView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetCoursesView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetTimetableView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetTimetableEntryView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class GetSchoolsView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    