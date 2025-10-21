from django.db import models
from django.core.exceptions import ValidationError

class Facility(models.Model):
    LAB = "Lab"
    WORKSHOP = "Workshop"
    TESTING_CENTER = "Testing Center"

    FACILITY_TYPE_CHOICES = [
        (LAB, "Lab"),
        (WORKSHOP, "Workshop"),
        (TESTING_CENTER, "Testing Center"),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    partner_org = models.CharField(max_length=200, blank=True)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPE_CHOICES)
    capabilities = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "location"], name="unique_facility_name_location"
            )
        ]

    def clean(self):
        
        """Validate that capabilities exist if services or equipment exist"""
        has_no_capabilities = not self.capabilities or not self.capabilities.strip()
        
        # Check if either services or equipment exist
        has_dependencies = False
        
        if self.pk:  # For saved objects, check the actual related objects
            has_dependencies = (self.services.exists() or self.equipment.exists())
        else:
            # For unsaved objects, use a flag that tests can set
            # This allows testing without database dependencies
            if hasattr(self, '_test_has_dependencies'):
                has_dependencies = self._test_has_dependencies
            # If no test flag, assume no dependencies for new unsaved objects
        
        # Rule: If dependencies exist, capabilities must be populated
        if has_dependencies and has_no_capabilities:
            raise ValidationError({
                'capabilities': 'Facility capabilities must be populated when Services/Equipment exist.'
            })
       
        
    def save(self, *args, **kwargs):
        self.full_clean()  # ✅ ensure clean() is triggered
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        """Prevent deletion if any dependent records exist"""
        if self.services.exists() or self.equipment.exists() or self.projects.exists():
            raise ValidationError(
                "Facility has dependent records (Services/Equipment/Projects)."
            )
        
        # If no dependencies, proceed with normal deletion
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.location})"
