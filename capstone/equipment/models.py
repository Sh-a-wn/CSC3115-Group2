from django.db import models
from django.core.exceptions import ValidationError
from facilities.models import Facility


class Equipment(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="equipment")
    name = models.CharField(max_length=200)
    capabilities = models.TextField(blank=True)
    description = models.TextField(blank=True)
    inventory_code = models.CharField(max_length=100, unique=True)
    usage_domain = models.CharField(
        max_length=50,
        choices=[
            ("Electronics", "Electronics"),
            ("Mechanical", "Mechanical"),
            ("IoT", "IoT"),
            ("Other", "Other"),
        ],
        default="Other",
    )
    support_phase = models.CharField(
        max_length=50,
        choices=[
            ("Training", "Training"),
            ("Prototyping", "Prototyping"),
            ("Testing", "Testing"),
            ("Commercialization", "Commercialization"),
        ],
        default="Training",
    )

    def __str__(self):
        return f"{self.name} ({self.inventory_code})"

    # ✅ Business Rule 1: Required fields
    def clean(self):
        """
        Business Rules:
        1️⃣ Facility, Name, and Inventory Code are required.
        2️⃣ Electronics equipment cannot have Training as its only support phase.
        """
        if not getattr(self, "facility", None) or not self.name or not self.inventory_code:
            raise ValidationError("Facility, name, and inventory code are required.")

        if self.usage_domain == "Electronics" and self.support_phase == "Training":
            raise ValidationError("Electronics equipment cannot be limited to the Training phase.")

    # ✅ Business Rule 2: Delete guard
    def delete(self, *args, **kwargs):
        """
        Prevent deletion if this equipment is referenced by a project.
        """
        try:
            from projects.models import Project
        except ImportError:
            # Allows test mocks to run without actual import dependency
            Project = None

        if Project:
            if Project.objects.filter(equipment_used=self).exists():
                raise ValidationError("Cannot delete equipment referenced by a project.")

        super().delete(*args, **kwargs)