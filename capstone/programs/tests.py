
from django.test import TestCase
from django.core.exceptions import ValidationError, IntegrityError
from .models import Program
from facilities.models import Facility
from projects.models import Project

class ProgramModelTests(TestCase):
	def test_create_program_with_required_fields(self):
		program = Program.objects.create(
			name="Test Program",
			description="A test program."
		)
		self.assertEqual(program.name, "Test Program")
		self.assertEqual(program.description, "A test program.")

	def test_program_missing_required_fields(self):
		with self.assertRaises(IntegrityError):
			Program.objects.create(description="Missing name")
		with self.assertRaises(IntegrityError):
			Program.objects.create(name="Missing description")


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
		# Should succeed
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
