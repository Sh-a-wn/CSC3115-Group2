from django.db import models

class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    partner_organization = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=100)  
    capabilities = models.TextField()  

    def __str__(self):
        return self.name

 
class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)  
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='equipment')  
    name = models.CharField(max_length=255)
    capabilities = models.TextField()  
    description = models.TextField()
    inventory_code = models.CharField(max_length=100, unique=True)
    usage_domain = models.CharField(max_length=100)  
    support_phase = models.CharField(max_length=100)  

    def __str__(self):
        return self.name