from django.db import models
from django.utils.translation import gettext_lazy as _

from programs.models import Program
from facilities.models import Facility


class Project(models.Model):
    class NatureOfProject(models.TextChoices):
        RESEARCH = "research", _("Research")
        PROTOTYPE = "prototype", _("Prototype")
        APPLIED = "applied", _("Applied Work")

    class PrototypeStage(models.TextChoices):
        CONCEPT = "concept", _("Concept")
        PROTOTYPE = "prototype", _("Prototype")
        MVP = "mvp", _("MVP")
        MARKET_LAUNCH = "market_launch", _("Market Launch")

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="projects")
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="projects")

    title = models.CharField(max_length=255)

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        COMPLETED = "completed", _("Completed")
        ON_HOLD = "on_hold", _("On Hold")
        CANCELLED = "cancelled", _("Cancelled")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    technical_requirements = models.CharField(max_length=255, blank=True)
    nature_of_project = models.CharField(
        max_length=20,
        choices=NatureOfProject.choices,
        default=NatureOfProject.RESEARCH,
    )
    description = models.TextField(blank=True)
    innovation_focus = models.CharField(max_length=255, blank=True)
    prototype_stage = models.CharField(
        max_length=20,
        choices=PrototypeStage.choices,
        default=PrototypeStage.CONCEPT,
    )
    testing_requirements = models.TextField(blank=True)
    commercialization_plan = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "program"], name="unique_project_title_per_program")
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        # Program and Facility are required (already enforced by DB)
        if not self.program_id or not self.facility_id:
            raise ValidationError("Project.ProgramId and Project.FacilityId are required.")

        # At least one participant
        if self.pk:
            if not self.participants.exists():
                raise ValidationError("Project must have at least one team member assigned.")

        # Completed projects must have at least one outcome
        if self.status == self.Status.COMPLETED and self.pk:
            if not self.outcomes.exists():
                raise ValidationError("Completed projects must have at least one documented outcome.")

        # Technical compatibility
        if self.technical_requirements and self.facility_id:
            facility = self.facility
            if facility.capabilities and self.technical_requirements.lower() not in facility.capabilities.lower():
                raise ValidationError("Project requirements not compatible with facility capabilities.")