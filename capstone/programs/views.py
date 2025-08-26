from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Program

class ProgramListView(ListView):
    model = Program

class ProgramDetailView(DetailView):
    model = Program

class ProgramCreateView(CreateView):
    model = Program
    fields = '_all_'
    success_url = reverse_lazy('program_list')

class ProgramUpdateView(UpdateView):
    model = Program
    fields = '_all_'
    success_url = reverse_lazy('program_list')

class ProgramDeleteView(DeleteView):
    model = Program
    success_url = reverse_lazy('program_list')