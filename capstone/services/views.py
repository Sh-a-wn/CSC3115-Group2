from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Service

class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"

class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
class ServiceCreateView(CreateView):
    model = Service
    fields = '__all__'
    template_name = "services/form.html"
    success_url = reverse_lazy('service_list')

class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'
    template_name = "services/form.html"
    success_url = reverse_lazy('service_list')

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "services/confirm_delete.html"
    success_url = reverse_lazy('service_list')

