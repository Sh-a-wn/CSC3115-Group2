from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Facility

class FacilityListView(ListView):
    model = Facility
    template_name = "facilities/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        facility_type = self.request.GET.get('type')

        if search:
            # search in name, location, and capabilities
            queryset = queryset.filter(name__icontains=search) | queryset.filter(location__icontains=search) | queryset.filter(capabilities__icontains=search)

        if facility_type and facility_type != "All":
            queryset = queryset.filter(facility_type=facility_type)

        return queryset

class FacilityDetailView(DetailView):
    model = Facility
    template_name = "facilities/detail.html"

class FacilityCreateView(CreateView):
    model = Facility
    fields = '__all__'
    template_name = "facilities/form.html"
    success_url = reverse_lazy('facility_list')

class FacilityUpdateView(UpdateView):
    model = Facility
    fields = '__all__'
    template_name = "facilities/form.html"
    success_url = reverse_lazy('facility_list')

class FacilityDeleteView(DeleteView):
    model = Facility
    template_name = "facilities/confirm_delete.html"
    success_url = reverse_lazy('facility_list')
