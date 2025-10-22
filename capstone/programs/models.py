from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Program(models.Model):
    VALID_ALIGNMENT_TOKENS = [('NDPIII', 'NDPIII'),
        ('DigitalRoadmap2023_2028', 'Digital Roadmap 2023-2028'),
        ('4IR', '4th Industrial Revolution') 
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    national_alignment = models.CharField(max_length=200, blank=True, choices=VALID_ALIGNMENT_TOKENS, verbose_name="National Alignemnt")
    focus_areas = models.TextField(blank=True)
    phases = models.CharField(max_length=200, blank=True)

    class Meta:
        # Ensure case-insensitive uniqueness of names
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_program_name',
            )
        ]

    def clean(self):
        # Required Fields Validation
        if not self.name:
            raise ValidationError({'name': _('Program.Name is required.')})
        if not self.description:
            raise ValidationError({'description': _('Program.Description is required.')})

        # National Alignment Validation
        if self.focus_areas and not self.national_alignment:
            raise ValidationError({
                'national_alignment': _(
                    'Program.NationalAlignment must include at least one recognized alignment when FocusAreas are specified.'
                )
            })

        # Validate alignment token if provided
        valid_tokens = [x[0] for x in self.VALID_ALIGNMENT_TOKENS]
        if self.national_alignment and self.national_alignment not in valid_tokens:
            raise ValidationError({'national_alignment': _('Invalid alignment token')})


        super().clean()

    def validate_unique(self, exclude=None):
        # Case-insensitive name uniqueness check
        if Program.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
            raise ValidationError({
                'name': _('Program.Name already exists.')
            })
        super().validate_unique(exclude)

    def delete(self, *args, **kwargs):
        # Lifecycle Protection
        if self.projects.exists():
            raise ValidationError(
                _('Program has Projects; archive or reassign before delete.')
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)