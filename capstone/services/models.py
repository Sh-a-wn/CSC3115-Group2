from django.db import models


from facilities.models import Facility

class Service(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    skill_type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
