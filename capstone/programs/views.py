from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Program

class ProgramListView(ListView):
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = Program.objects.all()

        search = self.request.GET.get('search', '')
        phase = self.request.GET.get('phase', '')
        alignment = self.request.GET.get('alignment', '')

        # General search across multiple fields
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(focus_areas__icontains=search)
            )

        # Filter by phase
        if phase and phase != 'All':
            queryset = queryset.filter(phases__iexact=phase)

        # Filter by national alignment
        if alignment and alignment != 'All':
            queryset = queryset.filter(national_alignment__iexact=alignment)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phases_list'] = Program.objects.values_list('phases', flat=True).distinct()
        context['alignments_list'] = Program.objects.values_list('national_alignment', flat=True).distinct()
        return context


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