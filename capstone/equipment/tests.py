from django.test import SimpleTestCase
from unittest.mock import Mock, patch, MagicMock
from django.core.exceptions import ValidationError
from equipment.models import Equipment


class EquipmentModelTest(SimpleTestCase):
    """Database-free tests for Equipment business rules."""

    def setUp(self):
        # Create a mock Facility that won't trigger database queries
        self.facility = MagicMock()
        self.facility._state = MagicMock()
        self.facility.pk = 1
        
        # Create Equipment without going through __init__ to bypass FK validation
        self.equipment = Equipment()
        # Set facility_id directly to avoid FK descriptor
        self.equipment.__dict__['facility_id'] = 1
        # Cache the facility object to prevent database lookups
        self.equipment._state.fields_cache = {'facility': self.facility}
        self.equipment.name = "Laser Cutter"
        self.equipment.inventory_code = "EQ-001"
        self.equipment.usage_domain = "Electronics"
        self.equipment.support_phase = "Testing"

    # 1️⃣ Required Fields Rule
    def test_required_fields(self):
        """Facility, Name, and InventoryCode must be provided."""
        eq = Equipment()
        eq._state.fields_cache = {}
        with self.assertRaises(ValidationError):
            eq.clean()

    # 2️⃣ Usage Domain vs Support Phase Rule
    def test_usage_domain_support_phase_coherence_valid(self):
        """Electronics with Testing or Prototyping should be valid."""
        self.equipment.usage_domain = "Electronics"
        self.equipment.support_phase = "Testing"
        try:
            self.equipment.clean()  # should not raise
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for valid combination.")

    def test_usage_domain_support_phase_coherence_invalid(self):
        """Electronics cannot have Training as only SupportPhase."""
        self.equipment.usage_domain = "Electronics"
        self.equipment.support_phase = "Training"
        with self.assertRaises(ValidationError) as cm:
            self.equipment.clean()
        self.assertIn("Electronics equipment cannot be limited to the Training phase", str(cm.exception))

    # 3️⃣ Delete Guard Rule — cannot delete if used by Project
    @patch('projects.models.Project')
    def test_delete_guard_prevents_deletion_if_referenced(self, MockProject):
        """Prevent deletion if Equipment is referenced by any project."""
        # Give equipment a pk so it's considered "saved"
        self.equipment.pk = 1
        
        # Mock Project.objects.filter().exists() to return True
        mock_queryset = Mock()
        mock_queryset.exists.return_value = True
        MockProject.objects.filter.return_value = mock_queryset
        
        # Mock the super().delete() to prevent database access
        with patch('django.db.models.Model.delete'):
            with self.assertRaises(ValidationError) as cm:
                self.equipment.delete()
            self.assertIn("Cannot delete equipment referenced by a project", str(cm.exception))

    @patch('projects.models.Project')
    def test_delete_guard_allows_deletion_if_not_referenced(self, MockProject):
        """Allow deletion if Equipment is not referenced."""
        # Give equipment a pk so it's considered "saved"
        self.equipment.pk = 1
        
        # Mock Project.objects.filter().exists() to return False
        mock_queryset = Mock()
        mock_queryset.exists.return_value = False
        MockProject.objects.filter.return_value = mock_queryset
        
        # Mock the super().delete() to prevent database access
        with patch('django.db.models.Model.delete'):
            try:
                self.equipment.delete()
            except ValidationError:
                self.fail("Deletion blocked unexpectedly when not referenced.")