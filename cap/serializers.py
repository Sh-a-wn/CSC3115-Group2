from rest_framework import serializers
from .models import Equipment, Facility

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'