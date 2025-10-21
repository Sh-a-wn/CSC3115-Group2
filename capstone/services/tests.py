import unittest
from unittest.mock import patch, Mock
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from services.models import Service


class ServiceModelTest(SimpleTestCase):
    def setUp(self):
        self.facility_id = 1

    def test_required_fields(self):
        service = Service()
        with self.assertRaises(ValidationError):
            service.full_clean()

    @patch("services.models.Service.objects")
    def test_scoped_uniqueness(self, mock_objects):
        mock_objects.filter.return_value.exclude.return_value.exists.return_value = True
        service = Service(facility_id=self.facility_id, name="PCB Fabrication", category="Testing", skill_type="Hardware")
        with self.assertRaises(ValidationError):
            service.clean()
            
    def test_delete_guard(self):
        service = Service(facility_id=self.facility_id, name="CNC", category="Testing", skill_type="Hardware")
        with patch.object(Service, "testing_requirements", create=True, new_callable=Mock) as mock_related:
            mock_related.exists.return_value = True
            with self.assertRaises(ValidationError):
                service.delete()

    def test_delete_guard_allows_delete_when_not_in_use(self):
        service = Service(facility_id=self.facility_id, name="CNC", category="Testing", skill_type="Hardware")
        with patch.object(Service, "testing_requirements", create=True, new_callable=Mock) as mock_related:
            mock_related.exists.return_value = False
            with patch("django.db.models.base.Model.delete", return_value=None) as mock_super_delete:
                service.delete()
                mock_super_delete.assert_called_once()