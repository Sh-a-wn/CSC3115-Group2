
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Participant, ProjectParticipant

# --- Participants ---
class ParticipantListView(ListView):
    model = Participant
    template_name = "participants/list.html"

class ParticipantDetailView(DetailView):
    model = Participant
    template_name = "participants/detail.html"

class ParticipantCreateView(CreateView):
    model = Participant
    fields = '__all__'
    template_name = "participants/form.html"
    success_url = reverse_lazy('participant_list')

class ParticipantUpdateView(UpdateView):
    model = Participant
    fields = '__all__'
    template_name = "participants/form.html"
    success_url = reverse_lazy('participant_list')

class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = "participants/confirm_delete.html"
    success_url = reverse_lazy('participant_list')


# --- Project Participants ---
class ProjectParticipantListView(ListView):
    model = ProjectParticipant
    template_name = "participants/project_list.html"

class ProjectParticipantDetailView(DetailView):
    model = ProjectParticipant
    template_name = "participants/project_detail.html"

class ProjectParticipantCreateView(CreateView):
    model = ProjectParticipant
    fields = '__all__'
    template_name = "participants/project_form.html"
    success_url = reverse_lazy('projectparticipant_list')

class ProjectParticipantUpdateView(UpdateView):
    model = ProjectParticipant
    fields = '__all__'
    template_name = "participants/project_form.html"
    success_url = reverse_lazy('projectparticipant_list')

class ProjectParticipantDeleteView(DeleteView):
    model = ProjectParticipant
    template_name = "participants/project_confirm_delete.html"
    success_url = reverse_lazy('projectparticipant_list')
