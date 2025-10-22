from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
from participants.models import Participant


class ParticipantModelTest(SimpleTestCase):
    """Database-free tests for Participant business rules."""

    def setUp(self):
        """Set up a valid participant instance for testing."""
        self.participant = Participant()
        self.participant.full_name = "John Doe"
        self.participant.email = "john.doe@example.com"
        self.participant.affiliation = "University of Technology"
        self.participant.specialization = "Software Engineering"
        self.participant.cross_skill_trained = False

    # 1️⃣ Required Fields Rule
    def test_required_fields_all_present(self):
        """All required fields present should pass validation."""
        try:
            self.participant.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when all required fields are present.")

    def test_required_fields_missing_full_name(self):
        """Missing FullName should raise ValidationError."""
        self.participant.full_name = ""
        with self.assertRaises(ValidationError) as cm:
            self.participant.clean()
        self.assertIn("Participant.FullName", str(cm.exception))

    def test_required_fields_missing_email(self):
        """Missing Email should raise ValidationError."""
        self.participant.email = ""
        with self.assertRaises(ValidationError) as cm:
            self.participant.clean()
        self.assertIn("Participant.Email", str(cm.exception))

    def test_required_fields_missing_affiliation(self):
        """Missing Affiliation should raise ValidationError."""
        self.participant.affiliation = ""
        with self.assertRaises(ValidationError) as cm:
            self.participant.clean()
        self.assertIn("Participant.Affiliation", str(cm.exception))

    def test_required_fields_all_missing(self):
        """All required fields missing should raise ValidationError."""
        participant = Participant()
        with self.assertRaises(ValidationError) as cm:
            participant.clean()
        error_message = str(cm.exception)
        self.assertIn("Participant.FullName", error_message)
        self.assertIn("Participant.Email", error_message)
        self.assertIn("Participant.Affiliation", error_message)

    # 2️⃣ Email Uniqueness Rule (tested via model constraint)
    def test_email_field_has_unique_constraint(self):
        """Email field should have unique=True constraint."""
        email_field = Participant._meta.get_field('email')
        self.assertTrue(email_field.unique, "Email field should have unique=True")

    # 3️⃣ Specialization Requirement for CrossSkillTrained
    def test_cross_skill_trained_valid_with_specialization(self):
        """CrossSkillTrained=True with Specialization should be valid."""
        self.participant.cross_skill_trained = True
        self.participant.specialization = "Data Science"
        try:
            self.participant.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when CrossSkillTrained has Specialization.")

    def test_cross_skill_trained_invalid_without_specialization(self):
        """CrossSkillTrained=True without Specialization should raise ValidationError."""
        self.participant.cross_skill_trained = True
        self.participant.specialization = None
        with self.assertRaises(ValidationError) as cm:
            self.participant.clean()
        self.assertIn("Cross-skill flag requires Specialization", str(cm.exception))

    def test_cross_skill_trained_invalid_with_empty_specialization(self):
        """CrossSkillTrained=True with empty Specialization should raise ValidationError."""
        self.participant.cross_skill_trained = True
        self.participant.specialization = ""
        with self.assertRaises(ValidationError) as cm:
            self.participant.clean()
        self.assertIn("Cross-skill flag requires Specialization", str(cm.exception))

    def test_cross_skill_trained_false_without_specialization(self):
        """CrossSkillTrained=False without Specialization should be valid."""
        self.participant.cross_skill_trained = False
        self.participant.specialization = None
        try:
            self.participant.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when CrossSkillTrained is False.")

    # Additional edge cases
    def test_optional_fields_can_be_empty(self):
        """Optional fields (phone, bio) can be empty."""
        self.participant.phone = None
        self.participant.bio = None
        try:
            self.participant.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for empty optional fields.")

    def test_specialization_can_be_set_without_cross_skill_trained(self):
        """Specialization can be set even when CrossSkillTrained is False."""
        self.participant.cross_skill_trained = False
        self.participant.specialization = "Machine Learning"
        try:
            self.participant.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when Specialization is set but CrossSkillTrained is False.")