from django.urls import path
from .views import EquipmentListCreateView, EquipmentDetailView, EquipmentByFacilityView

urlpatterns = [
    path('', EquipmentListCreateView.as_view(), name='equipment-list-create'),
    path('<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail'),
    path('facilities/<int:facility_id>/equipment/', EquipmentByFacilityView.as_view(), name='equipment-by-facility'),
]