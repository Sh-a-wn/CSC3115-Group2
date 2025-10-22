from django.db import models
from projects.models import Project 
from django.core.exceptions import ValidationError

class Participant(models.Model):
    AFFILIATIONS = [
        ("CS", "Computer Science"),
        ("SE", "Software Engineering"),
        ("Eng", "Engineering"),
        ("Other", "Other"),
    ]

    SPECIALIZATIONS = [
        ("Software", "Software"),
        ("Hardware", "Hardware"),
        ("Business", "Business"),
    ]

    INSTITUTIONS = [
        ("SCIT", "SCIT"),
        ("CEDAT", "CEDAT"),
        ("UniPod", "UniPod"),
        ("UIRI", "UIRI"),
        ("Lwera", "Lwera"),
    ]

    ROLE_CHOICES = [
        ("Student", "Student"),
        ("Lecturer", "Lecturer"),
        ("Contributor", "Contributor"),
    ]

    SKILL_ROLES = [
        ("Developer", "Developer"),
        ("Engineer", "Engineer"),
        ("Designer", "Designer"),
        ("Business Lead", "Business Lead"),
    ]

    # fields
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    affiliation = models.CharField(max_length=50, choices=AFFILIATIONS)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS)
    cross_skill_trained = models.BooleanField(default=False)
    institution = models.CharField(max_length=50, choices=INSTITUTIONS)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="participants")
    role_on_project = models.CharField(max_length=50, choices=ROLE_CHOICES)
    skill_role = models.CharField(max_length=50, choices=SKILL_ROLES)

    def __str__(self):
        return f"{self.full_name} → {self.project.name} ({self.role_on_project}, {self.skill_role})"
    def clean(self):
        """
        Business Rules:
        1️⃣ FullName, Email, and Affiliation are required.
        2️⃣ Email must be unique (handled by model field constraint).
        3️⃣ CrossSkillTrained can only be True if Specialization is set.
        """
        # Rule 1: Required fields
        if not self.full_name or not self.email or not self.affiliation:
            raise ValidationError(
                "Participant.FullName, Participant.Email, and Participant.Affiliation are required."
            )

        # Rule 3: Cross-skill training requires specialization
        if self.cross_skill_trained and not self.specialization:
            raise ValidationError("Cross-skill flag requires Specialization.")

    def save(self, *args, **kwargs):
        """Override save to ensure clean() is called."""
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['full_name']
        verbose_name = "Participant"
        verbose_name_plural = "Participants"