
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Program
from facilities.models import Facility
from projects.models import Project

class ProgramModelTests(TestCase):
	def test_program_missing_required_fields(self):
		# Missing name
		program = Program(description="Missing name")
		with self.assertRaises(ValidationError):
			program.full_clean()
		# Missing description
		program = Program(name="Missing description")
		with self.assertRaises(ValidationError):
			program.full_clean()
    


class ProjectReferentialIntegrityTests(TestCase):
	def setUp(self):
		self.program = Program.objects.create(
			name="Ref Integrity Program",
			description="Program for referential integrity test."
		)
		self.facility = Facility.objects.create(
			name="Test Facility",
			location="Test Location"
		)

	def test_project_must_have_facility_and_program(self):
		project = Project.objects.create(
			title="Test Project",
			program=self.program,
			facility=self.facility
		)
		self.assertEqual(project.program, self.program)
		self.assertEqual(project.facility, self.facility)

	def test_project_missing_facility(self):
		with self.assertRaises(IntegrityError):
			Project.objects.create(
				title="No Facility",
				program=self.program
			)

	def test_project_missing_program(self):
		with self.assertRaises(IntegrityError):
			Project.objects.create(
				title="No Program",
				facility=self.facility
			)
