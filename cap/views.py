from django.shortcuts import render

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Equipment
from .serializers import EquipmentSerializer

class EquipmentListCreateView(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['facility__facility_id', 'usage_domain']  
    search_fields = ['capabilities', 'name']  

class EquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class EquipmentByFacilityView(generics.ListAPIView):
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        facility_id = self.kwargs['facility_id']
        return Equipment.objects.filter(facility__facility_id=facility_id)
