from django.urls import path
from .views import (
    EquipmentListView, EquipmentDetailView,
    EquipmentCreateView, EquipmentUpdateView, EquipmentDeleteView
)

urlpatterns = [
    path('', EquipmentListView.as_view(), name='equipment_list'),
    path('add/', EquipmentCreateView.as_view(), name='equipment_add'),
    path('<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('<int:pk>/edit/', EquipmentUpdateView.as_view(), name='equipment_edit'),
    path('<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),
]
