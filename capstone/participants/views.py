from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Participant

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
