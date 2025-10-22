from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.db import models as dj_models
from unittest.mock import Mock

from projects.models import Project


class ProjectBusinessRulesTest(SimpleTestCase):
    """Tests for project business rules using mocks.

    We create Project instances (not saved) and set the attributes and related
    managers (participants, outcomes) to Mock objects that control the
    behavior of .exists(). This avoids using the test database.
    """ 

    def make_project(self, **overrides):
        # Return a plain object that has the attributes the Project.clean expects.
        class Dummy:
            pass

        p = Dummy()
        # Primitive attributes
        p.pk = overrides.get("pk", 1)
        p.program_id = overrides.get("program_id", 1)
        p.facility_id = overrides.get("facility_id", 1)
        p.title = overrides.get("title", "Test Project")
        p.status = overrides.get("status", Project.Status.ACTIVE)
        # Provide class-like reference used inside Project.clean
        p.Status = Project.Status
        p.technical_requirements = overrides.get("technical_requirements", "")
        # Related manager-like mocks
        p.participants = overrides.get("participants", Mock())
        p.outcomes = overrides.get("outcomes", Mock())
        # Facility object used in compatibility check
        p.facility = overrides.get("facility", Mock(capabilities=overrides.get("facility_capabilities", "CNC")))
        return p

    def test_completed_project_requires_outcome(self):
        # Participant exists, outcome does not exist -> should raise outcome error
        participants = Mock()
        participants.exists.return_value = True
        outcomes = Mock()
        outcomes.exists.return_value = False

        project = self.make_project(status=Project.Status.COMPLETED, participants=participants, outcomes=outcomes)

        with self.assertRaisesMessage(ValidationError, "Completed projects must have at least one documented outcome."):
            Project.clean(project)

        # Now outcomes exist -> clean should not raise
        outcomes.exists.return_value = True
        Project.clean(project)

    def test_project_requires_participant(self):
        participants = Mock()
        participants.exists.return_value = False
        outcomes = Mock()
        outcomes.exists.return_value = False

        project = self.make_project(participants=participants, outcomes=outcomes)

        with self.assertRaisesMessage(ValidationError, "Project must have at least one team member assigned."):
            Project.clean(project)

        participants.exists.return_value = True
        Project.clean(project)

    def test_unique_project_name_per_program_constraint_present(self):
        # Verify the model declares a UniqueConstraint on (title, program)
        constraints = getattr(Project._meta, "constraints", [])
        found = False
        for c in constraints:
            if isinstance(c, dj_models.UniqueConstraint):
                fields = tuple(getattr(c, "fields", []))
                if tuple(fields) == ("title", "program") or set(fields) == {"title", "program"}:
                    found = True
                    break
        self.assertTrue(found, "UniqueConstraint(title, program) not found on Project._meta.constraints")

    def test_technical_compatibility(self):
        participants = Mock(); participants.exists.return_value = True
        outcomes = Mock(); outcomes.exists.return_value = False

        # Facility capabilities don't include PCB Fabrication
        project = self.make_project(participants=participants, outcomes=outcomes, technical_requirements="PCB Fabrication", facility_capabilities="CNC")
        with self.assertRaisesMessage(ValidationError, "Project requirements not compatible with facility capabilities."):
            Project.clean(project)

        # Compatible requirement
        project.technical_requirements = "CNC"
        Project.clean(project)
