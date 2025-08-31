from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Equipment

class EquipmentListView(ListView):
    model = Equipment
    template_name = "equipment/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        domain = self.request.GET.get('domain')

        if search:
            queryset = queryset.filter(capabilities__icontains=search)

        if domain and domain != "All":
            queryset = queryset.filter(usage_domain=domain)

        return queryset

class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = "equipment/detail.html"

class EquipmentCreateView(CreateView):
    model = Equipment
    fields = ['facility', 'name', 'capabilities', 'description', 'inventory_code', 'usage_domain', 'support_phase']
    template_name = "equipment/form.html"
    success_url = reverse_lazy('equipment_list')

class EquipmentUpdateView(UpdateView):
    model = Equipment
    fields = ['facility', 'name', 'capabilities', 'description', 'inventory_code', 'usage_domain', 'support_phase']
    template_name = "equipment/form.html"
    success_url = reverse_lazy('equipment_list')

class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = "equipment/confirm_delete.html"
    success_url = reverse_lazy('equipment_list')
