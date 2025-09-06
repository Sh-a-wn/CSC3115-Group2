from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Outcome
from projects.models import Project


class OutcomeListForProjectView(ListView):
    template_name = "outcome/outcome_list_for_project.html"

    def get_queryset(self):
        self.project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        return Outcome.objects.filter(project=self.project).order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["project"] = self.project
        return ctx


class OutcomeDetailView(DetailView):
    model = Outcome
    template_name = "outcome/outcome_detail.html"

class OutcomeCreateView(CreateView):
    model = Outcome
    fields = "__all__"
    template_name = "outcome/outcome_form.html"

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.kwargs.get("project_id")
        if project_id:
            initial["project"] = get_object_or_404(Project, pk=project_id)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "project_id" in self.kwargs:
            context["project"] = get_object_or_404(Project, pk=self.kwargs["project_id"])
        return context

    def form_valid(self, form):
        if "project_id" in self.kwargs:
            form.instance.project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("project_outcomes", kwargs={"project_id": self.object.project_id})


class OutcomeUpdateView(UpdateView):
    model = Outcome
    fields = "__all__"
    template_name = "outcome/outcome_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "project_id" in self.kwargs:
            context["project"] = get_object_or_404(Project, pk=self.kwargs["project_id"])
        else:
            # If no project_id in kwargs, get it from the outcome object
            context["project"] = self.object.project
        return context
    
    def form_valid(self, form):
        if "project_id" in self.kwargs:
            form.instance.project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("project_outcomes", kwargs={"project_id": self.object.project_id})

class OutcomeDeleteView(DeleteView):
    model = Outcome
    template_name = "outcome/outcome_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("project_outcomes", kwargs={"project_id": self.object.project_id})