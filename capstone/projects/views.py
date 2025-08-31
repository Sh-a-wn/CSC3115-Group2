from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Project
from programs.models import Program
from facilities.models import Facility


class ProjectListView(ListView):
    model = Project
    ordering = ["-created_at"]


class ProjectDetailView(DetailView):
    model = Project


class ProjectCreateView(CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("project_list")


class ProjectUpdateView(UpdateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("project_list")


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("project_list")


class ProjectsByFacilityView(ListView):
    template_name = "projects/project_list_by_facility.html"

    def get_queryset(self):
        facility = get_object_or_404(Facility, pk=self.kwargs["facility_id"])
        return Project.objects.filter(facility=facility).order_by("-created_at")


class ProjectsByProgramView(ListView):
    template_name = "projects/project_list_by_program.html"

    def get_queryset(self):
        program = get_object_or_404(Program, pk=self.kwargs["program_id"])
        return Project.objects.filter(program=program).order_by("-created_at")