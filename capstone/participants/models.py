
from django.db import models
from projects.models import Project  

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

    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    affiliation = models.CharField(max_length=50, choices=AFFILIATIONS)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS)
    cross_skill_trained = models.BooleanField(default=False)
    institution = models.CharField(max_length=50, choices=INSTITUTIONS)

    def __str__(self):
        return f"{self.full_name} ({self.affiliation})"


class ProjectParticipant(models.Model):
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

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_participants")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="project_participations")

    role_on_project = models.CharField(max_length=50, choices=ROLE_CHOICES)
    skill_role = models.CharField(max_length=50, choices=SKILL_ROLES)

    def __str__(self):
        return f"{self.participant.full_name} → {self.project.name} ({self.role_on_project}, {self.skill_role})"
