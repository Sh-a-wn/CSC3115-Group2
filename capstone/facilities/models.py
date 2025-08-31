from django.db import models

class Facility(models.Model):
    FACILITY_TYPES = [
        ("Lab", "Lab"),
        ("Workshop", "Workshop"),
        ("Testing Center", "Testing Center"),
    ]

    CAPABILITIES = [
        ("CNC", "CNC"),
        ("PCB Fabrication", "PCB Fabrication"),
        ("Materials Testing", "Materials Testing"),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    partner_organization = models.CharField(max_length=200, blank=True)

    facility_type = models.CharField(
        max_length=50,
        choices=FACILITY_TYPES,
        default="Lab"
    )

    capabilities = models.CharField(
        max_length=50,
        choices=CAPABILITIES,
        default="CNC"
    )

    def __str__(self):
        return f"{self.name} ({self.facility_type})"
