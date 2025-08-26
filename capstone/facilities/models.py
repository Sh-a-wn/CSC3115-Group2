
from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    partner_org = models.CharField(max_length=200, blank=True)
    facility_type = models.CharField(max_length=100, blank=True)
    capabilities = models.TextField(blank=True)

    def __str__(self):
        return self.name
