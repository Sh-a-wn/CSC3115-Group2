from rest_framework import serializers
from .models import Equipment, Facility

class EquipmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label="Equipment Name")
    capabilities = serializers.CharField(label="Key Capabilities")
    description = serializers.CharField(label="Detailed Description")
    inventory_code = serializers.CharField(label="Inventory Code")
    usage_domain = serializers.CharField(label="Domain (Electronics, Mechanical, IoT, etc.)")
    support_phase = serializers.CharField(label="Support Phase (Training, Prototyping, etc.)")
    
    
    class Meta:
        model = Equipment
        fields = '__all__'