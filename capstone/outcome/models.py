from django.db import models
from django.utils.translation import gettext_lazy as _

from projects.models import Project


class Outcome(models.Model):
    class OutcomeType(models.TextChoices):
        CAD = "cad", _("CAD")
        PCB = "pcb", _("PCB")
        PROTOTYPE = "prototype", _("Prototype")
        REPORT = "report", _("Report")
        BUSINESS_PLAN = "business_plan", _("Business Plan")

    class CommercializationStatus(models.TextChoices):
        DEMOED = "demoed", _("Demoed")
        MARKET_LINKED = "market_linked", _("Market Linked")
        LAUNCHED = "launched", _("Launched")

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="outcomes")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    artifact_link = models.URLField(blank=True)  # URL only per instruction
    outcome_type = models.CharField(max_length=30, choices=OutcomeType.choices)
    quality_certification = models.CharField(max_length=255, blank=True)
    commercialization_status = models.CharField(
        max_length=30,
        choices=CommercializationStatus.choices,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.get_outcome_type_display()})"