from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from medical_appointments.models import MedicalSpeciality

from .serializers import MedicalSpecialitySerializer


class MedicalSpecialityViewSet(viewsets.ModelViewSet):
    queryset = MedicalSpeciality.objects.all()
    serializer_class = MedicalSpecialitySerializer
    permission_classes = [IsAuthenticated]
