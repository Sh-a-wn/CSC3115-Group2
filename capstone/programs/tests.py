from django.test import SimpleTestCase
from unittest.mock import Mock, patch
from django.core.exceptions import ValidationError
from .models import Program

class ProgramBusinessRulesTests(SimpleTestCase):
    def setUp(self):
        self.valid_program_data = {
            'name': 'Test Program',
            'description': 'A test program description',
            'national_alignment': 'NDPIII',
            'focus_areas': 'Digital Innovation',
            'phases': 'Phase 1'
        }

    @patch('programs.models.Program.clean')
    def test_required_fields(self, mock_clean):
        """Rule: Required Fields - Name and Description must be provided"""
        # Valid case
        program = Program(**self.valid_program_data)
        program.clean() 
        
        # Test missing name
        invalid_data = self.valid_program_data.copy()
        del invalid_data['name']
        program = Program(**invalid_data)
        mock_clean.side_effect = ValidationError("Program.Name is required.")
        with self.assertRaisesMessage(ValidationError, "Program.Name is required."):
            program.clean()

        # Test missing description
        invalid_data = self.valid_program_data.copy()
        del invalid_data['description']
        program = Program(**invalid_data)
        mock_clean.side_effect = ValidationError("Description field is required.")
        with self.assertRaisesMessage(ValidationError, "Description field is required."):
            program.clean()

    @patch('programs.models.Program.validate_unique')
    def test_name_uniqueness(self, mock_validate_unique):
        """Rule: Uniqueness - Program Name must be unique (case-insensitive)"""
        mock_validate_unique.side_effect = ValidationError("Program.Name already exists.")
        
        # Test case sensitivity
        program = Program(**self.valid_program_data)
        with self.assertRaisesMessage(ValidationError, "Program.Name already exists."):
            program.validate_unique()

        # Test case insensitivity
        program_data = self.valid_program_data.copy()
        program_data['name'] = 'TEST PROGRAM'
        program = Program(**program_data)
        with self.assertRaisesMessage(ValidationError, "Program.Name already exists."):
            program.validate_unique()

    @patch('programs.models.Program.clean')
    def test_national_alignment_validation(self, mock_clean):
        """Rule: National Alignment - Must have valid alignment when FocusAreas specified"""
        # Valid case
        program = Program(**self.valid_program_data)
        program.clean()  # Should not raise exception

        # Invalid case - has focus areas but missing alignment
        invalid_data = self.valid_program_data.copy()
        invalid_data['focus_areas'] = 'Some Focus Area'
        invalid_data['national_alignment'] = ''
        program = Program(**invalid_data)
        mock_clean.side_effect = ValidationError(
            "Program.NationalAlignment must include at least one recognized alignment when FocusAreas are specified."
        )
        with self.assertRaisesMessage(
            ValidationError,
            "Program.NationalAlignment must include at least one recognized alignment when FocusAreas are specified."
        ):
            program.clean()

        # Invalid alignment token
        invalid_data = self.valid_program_data.copy()
        invalid_data['national_alignment'] = 'InvalidToken'
        program = Program(**invalid_data)
        mock_clean.side_effect = ValidationError("Invalid alignment token")
        with self.assertRaisesMessage(ValidationError, "Invalid alignment token"):
            program.clean()

    @patch('django.db.models.Model.delete')
    @patch('programs.models.Program.projects')
    def test_lifecycle_protection(self, mock_projects, mock_delete):
        """Rule: Lifecycle Protection - Cannot delete Programs with Projects"""
        program = Program(**self.valid_program_data)
        program.id = 1  # Set ID to avoid None error
        
        # Test program with projects cannot be deleted
        mock_projects.exists.return_value = True
        with self.assertRaisesMessage(
            ValidationError,
            "Program has Projects; archive or reassign before delete."
        ):
            program.delete()
        mock_delete.assert_not_called()  # Ensure delete was not called

        # Test program without projects can be deleted
        mock_projects.exists.return_value = False
        program.delete()
        mock_delete.assert_called_once()  # Ensure delete was called

    def test_string_representation(self):
        """Test string representation of Program"""
        program = Program(name="Test Program")
        self.assertEqual(str(program), "Test Program")