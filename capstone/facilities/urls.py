from django.urls import path
from .views import *

urlpatterns = [
    path('', FacilityListView.as_view(), name='facility_list'),
    path('add/', FacilityCreateView.as_view(), name='facility_add'),
    path('<int:pk>/', FacilityDetailView.as_view(), name='facility_detail'),
    path('<int:pk>/edit/', FacilityUpdateView.as_view(), name='facility_edit'),
    path('<int:pk>/delete/', FacilityDeleteView.as_view(), name='facility_delete'),
]
