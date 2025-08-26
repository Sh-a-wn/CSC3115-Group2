from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Service

class ServiceListView(ListView):
    model = Service

class ServiceDetailView(DetailView):
    model = Service

class ServiceCreateView(CreateView):
    model = Service
    fields = '__all__'
    success_url = reverse_lazy('service_list')

class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'
    success_url = reverse_lazy('service_list')

class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('service_list')
