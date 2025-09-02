from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Program

class ProgramListView(ListView):
    model = Program

class ProgramDetailView(DetailView):
    model = Program

class ProgramCreateView(CreateView):
    model = Program
    fields = ['name', 'description', 'national_alignment', 'focus_areas', 'phases']
    template_name = 'programs/add_program.html'
    success_url = '/programs/' 

class ProgramUpdateView(UpdateView):
    model = Program
    fields = '__all__'
    success_url = reverse_lazy('program_list')

class ProgramDeleteView(DeleteView):
    model = Program
    success_url = reverse_lazy('program_list')