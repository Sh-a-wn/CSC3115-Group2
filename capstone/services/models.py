from django.db import models
from django.core.exceptions import ValidationError
from facilities.models import Facility


class Service(models.Model):
    TRAINING = "Training"
    CONSULTING = "Consulting"
    MAINTENANCE = "Maintenance"
    OTHER = "Other"

    CATEGORY_CHOICES = [
        (TRAINING, "Training"),
        (CONSULTING, "Consulting"),
        (MAINTENANCE, "Maintenance"),
        (OTHER, "Other"),
    ]

    SOFTWARE = "Software"
    HARDWARE = "Hardware"
    BUSINESS = "Business"
    OTHER_SKILL = "Other"

    SKILL_TYPE_CHOICES = [
        (SOFTWARE, "Software"),
        (HARDWARE, "Hardware"),
        (BUSINESS, "Business"),
        (OTHER_SKILL, "Other"),
    ]

    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT, related_name="services"
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    skill_type = models.CharField(max_length=50, choices=SKILL_TYPE_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "name"], name="unique_service_per_facility"
            )
        ]

    def delete(self, *args, **kwargs):
        if self.testing_requirements.exists():
            raise ValidationError(
                f"Cannot delete service. A project depends on category {self.category}."
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.facility.name})"

    def clean(self):
        # Enforce scoped uniqueness (name within the same facility)
        if self.facility_id and self.name:
            if Service.objects.filter(
                facility_id=self.facility_id,
                name=self.name
            ).exclude(pk=self.pk).exists():
                raise ValidationError(
                    "A service with this name already exists in this facility."
                )

class TestingRequirement(models.Model):
    """Links a Project to a Service it depends on for testing."""

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="service_requirements"
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="testing_requirements"
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("project", "service")

    def __str__(self):
        return f"{self.project.title} requires {self.service.name}"
