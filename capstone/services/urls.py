from django.urls import path
from .views import *

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('add/', ServiceCreateView.as_view(), name='service_add'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_edit'),
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
]
