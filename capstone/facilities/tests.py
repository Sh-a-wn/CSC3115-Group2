from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from unittest.mock import MagicMock, patch
from facilities.models import Facility

class FacilityModelTest(SimpleTestCase):
    def setUp(self):
        self.facility = Facility(
            name="UIRI Lab",
            location="Kampala",
            facility_type=Facility.LAB,
            capabilities="CNC, PCB fabrication",
        )

    def test_capabilities_required_if_services_exist(self):
        """Test capabilities required when services exist"""
        f = Facility(
            name="CEDAT Workshop",
            location="Makerere",
            facility_type=Facility.WORKSHOP,
            capabilities=""  # EMPTY
        )
        f._test_has_dependencies = True  # Simulate having services
        
        with self.assertRaises(ValidationError) as cm:
            f.clean()
        self.assertIn("capabilities must be populated", str(cm.exception))

    def test_capabilities_required_if_equipment_exist(self):
        """Test capabilities required when equipment exists"""
        f = Facility(
            name="Equipment Only Lab",
            location="Kampala",
            facility_type=Facility.LAB,
            capabilities=""  # EMPTY
        )
        f._test_has_dependencies = True  # Simulate having equipment
        
        with self.assertRaises(ValidationError):
            f.clean()

    def test_capabilities_required_if_both_exist(self):
        """Test capabilities required when both services AND equipment exist"""
        f = Facility(
            name="Busy Facility",
            location="Entebbe",
            facility_type=Facility.WORKSHOP,
            capabilities=""  # EMPTY
        )
        f._test_has_dependencies = True  # Simulate having both
        
        with self.assertRaises(ValidationError):
            f.clean()

    def test_capabilities_not_required_when_no_dependencies(self):
        """Test empty capabilities allowed when no services or equipment"""
        f = Facility(
            name="New Empty Facility",
            location="Jinja",
            facility_type=Facility.LAB,
            capabilities=""  # EMPTY - should be allowed
        )
        f._test_has_dependencies = False  # No dependencies
        
        # Should NOT raise ValidationError
        try:
            f.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError when no dependencies exist")

    def test_capabilities_allowed_when_populated(self):
        """Test capabilities work when populated (even with dependencies)"""
        f = Facility(
            name="Proper Facility",
            location="Gulu",
            facility_type=Facility.LAB,
            capabilities="CNC, 3D Printing, Laser Cutting"  # POPULATED
        )
        f._test_has_dependencies = True  # Has dependencies but also has capabilities
        
        # Should NOT raise ValidationError
        try:
            f.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError when capabilities are populated")

    

    def test_none_capabilities_treated_as_empty(self):
        """Test that None capabilities is treated as empty"""
        f = Facility(
            name="None Capabilities Facility",
            location="Soroti",
            facility_type=Facility.LAB,
            capabilities=None  # None value
        )
        f._test_has_dependencies = True
        
        with self.assertRaises(ValidationError):
            f.clean()
            
    def test_delete_blocked_if_services_exist(self):
        """Test deletion blocked when services depend on facility"""
        mock_services = MagicMock()
        mock_services.exists.return_value = True
        mock_equipment = MagicMock()
        mock_equipment.exists.return_value = False  # No equipment
        mock_projects = MagicMock()
        mock_projects.exists.return_value = False   # No projects

        with patch.object(Facility, "services", mock_services):
            with patch.object(Facility, "equipment", mock_equipment):
                with patch.object(Facility, "projects", mock_projects):
                    with self.assertRaises(ValidationError) as cm:
                        self.facility.delete()
                    # Optional: Verify error message
                    self.assertIn("dependent records", str(cm.exception))

    def test_delete_blocked_if_equipment_exist(self):
        """Test deletion blocked when equipment depends on facility"""
        mock_services = MagicMock()
        mock_services.exists.return_value = False   # No services
        mock_equipment = MagicMock()
        mock_equipment.exists.return_value = True   # Equipment exists!
        mock_projects = MagicMock()
        mock_projects.exists.return_value = False   # No projects

        with patch.object(Facility, "services", mock_services):
            with patch.object(Facility, "equipment", mock_equipment):
                with patch.object(Facility, "projects", mock_projects):
                    with self.assertRaises(ValidationError):
                        self.facility.delete()

    def test_delete_blocked_if_projects_exist(self):
        """Test deletion blocked when projects depend on facility"""
        mock_services = MagicMock()
        mock_services.exists.return_value = False   # No services
        mock_equipment = MagicMock()
        mock_equipment.exists.return_value = False  # No equipment
        mock_projects = MagicMock()
        mock_projects.exists.return_value = True    # Projects exist!

        with patch.object(Facility, "services", mock_services):
            with patch.object(Facility, "equipment", mock_equipment):
                with patch.object(Facility, "projects", mock_projects):
                    with self.assertRaises(ValidationError):
                        self.facility.delete()
    
    def test_delete_allowed_when_no_dependencies(self):
        """Test deletion succeeds when no dependencies exist"""
        mock_services = MagicMock()
        mock_services.exists.return_value = False   # No services
        mock_equipment = MagicMock()
        mock_equipment.exists.return_value = False  # No equipment  
        mock_projects = MagicMock()
        mock_projects.exists.return_value = False   # No projects

        with patch.object(Facility, "services", mock_services):
            with patch.object(Facility, "equipment", mock_equipment):
                with patch.object(Facility, "projects", mock_projects):
                    # Mock the actual database deletion
                    with patch("django.db.models.base.Model.delete") as mock_super_delete:
                        self.facility.delete()
                        # Verify the parent delete method was called
                        mock_super_delete.assert_called_once()
            

    @patch('django.db.models.base.Model.validate_constraints')
    def test_required_fields_missing(self, mock_validate):
        """Test validation fails when required fields are missing"""
        mock_validate.return_value = None  # Skip constraint validation
        
        f = Facility()
        with self.assertRaises(ValidationError) as cm:
            f.full_clean()
        
        # Verify all 3 required fields are in the errors
        errors = cm.exception.error_dict
        required_fields = ['name', 'location', 'facility_type']
        for field in required_fields:
            self.assertIn(field, errors)

    @patch('django.db.models.base.Model.validate_constraints') 
    def test_required_fields_provided(self, mock_validate):
        """Test validation passes when required fields are provided"""
        mock_validate.return_value = None  # Skip constraint validation
        
        f = Facility(
            name="UIRI Lab",
            location="Kampala",
            facility_type=Facility.LAB
        )
        
        try:
            f.full_clean()  # Should not raise ValidationError
        except ValidationError:
            self.fail("ValidationError raised with all required fields provided")
            
    @patch('django.db.models.query.QuerySet.exists')
    def test_unique_name_location(self, mock_exists):
        # Mock that a duplicate EXISTS (returns True)
        mock_exists.return_value = True
        
        f1 = Facility(
            name="UIRI Lab",
            location="Kampala",
            facility_type=Facility.LAB,
        )
        
        with self.assertRaises(ValidationError) as context:
            f1.full_clean()
        
        self.assertIn('__all__', context.exception.message_dict)
        error_message = context.exception.message_dict['__all__'][0]
        self.assertIn('Name and Location already exists', error_message)
    
    @patch('django.db.models.query.QuerySet.exists')
    def test_same_name_different_location_allowed(self, mock_exists):
        # Mock that NO duplicate exists (returns False)
        mock_exists.return_value = False
        
        f1 = Facility(
            name="UIRI Lab",
            location="Kampala",
            facility_type=Facility.LAB,
        )
        
        # Should not raise an exception
        try:
            f1.full_clean()
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly")