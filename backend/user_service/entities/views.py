from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import UserSerializer
from .models import 


class ListUniversitiesView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

