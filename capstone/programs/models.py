from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    national_alignment = models.CharField(max_length=200, blank=True)
    focus_areas = models.TextField(blank=True)
    phases = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name