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