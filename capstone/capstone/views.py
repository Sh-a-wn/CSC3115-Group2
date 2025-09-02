from django.shortcuts import render
from projects.models import Project
from participants.models import Participant
from facilities.models import Facility
from equipment.models import Equipment
from services.models import Service
from outcome.models import Outcome
from programs.models import Program

def dashboard(request):
    context = {
        "total_projects": Project.objects.count(),
        "total_programs": Program.objects.count(),
        "total_participants": Participant.objects.count(),
        "total_facilities": Facility.objects.count(),
        "total_equipment": Equipment.objects.count(),
        "total_services": Service.objects.count(),
        "total_outcome": Outcome.objects.count(),
    }
    return render(request, "dashboard.html", context)
