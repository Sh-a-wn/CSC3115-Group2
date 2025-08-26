from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Facility

class FacilityListView(ListView):
    model = Facility

class FacilityDetailView(DetailView):
    model = Facility

class FacilityCreateView(CreateView):
    model = Facility
    fields = '__all__'
    success_url = reverse_lazy('facility_list')

class FacilityUpdateView(UpdateView):
    model = Facility
    fields = '__all__'
    success_url = reverse_lazy('facility_list')

class FacilityDeleteView(DeleteView):
    model = Facility
    success_url = reverse_lazy('facility_list')
