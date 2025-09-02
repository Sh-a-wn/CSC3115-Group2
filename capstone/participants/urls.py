from django.urls import path
from .views import (
    ParticipantListView, ParticipantDetailView,
    ParticipantCreateView, ParticipantUpdateView, ParticipantDeleteView
)

urlpatterns = [
    path('', ParticipantListView.as_view(), name='participant_list'),
    path('add/', ParticipantCreateView.as_view(), name='participant_add'),
    path('<int:pk>/', ParticipantDetailView.as_view(), name='participant_detail'),
    path('<int:pk>/edit/', ParticipantUpdateView.as_view(), name='participant_edit'),
    path('<int:pk>/delete/', ParticipantDeleteView.as_view(), name='participant_delete'),
]
