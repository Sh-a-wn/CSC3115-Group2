from django.db import models


from facilities.models import Facility

class Service(models.Model):
    CATEGORIES = [
        ("Machining", "Machining"),
        ("Training", "Training"),
        ("Testing", "Testing"),
    ]
    SKILL_TYPE = [
        ("Hardware", "Hardware"),
        ("Software", "Software"),
        ("Integration", "Integration"),
    ]
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=100, 
        choices=CATEGORIES,
        default="General")
    skill_type = models.CharField(
        max_length=100, 
        choices=SKILL_TYPE,
        default="Hardware")
    

    def __str__(self):
        return self.name
