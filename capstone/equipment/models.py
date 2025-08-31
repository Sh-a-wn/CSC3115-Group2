
from django.db import models
from facilities.models import Facility

class Equipment(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="equipment")
    name = models.CharField(max_length=200)
    capabilities = models.TextField(blank=True)  # functions it can perform
    description = models.TextField(blank=True)   # overview of purpose
    inventory_code = models.CharField(max_length=100, unique=True)  # tracking code
    usage_domain = models.CharField(
        max_length=50,
        choices=[
            ("Electronics", "Electronics"),
            ("Mechanical", "Mechanical"),
            ("IoT", "IoT"),
            ("Other", "Other"),
        ],
        default="Other"
    )
    support_phase = models.CharField(
        max_length=50,
        choices=[
            ("Training", "Training"),
            ("Prototyping", "Prototyping"),
            ("Testing", "Testing"),
            ("Commercialization", "Commercialization"),
        ],
        default="Training"
    )

    def __str__(self):
        return f"{self.name} ({self.inventory_code})"
