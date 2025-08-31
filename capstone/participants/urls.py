from django.urls import path
from .views import (
    ParticipantListView, ParticipantDetailView, ParticipantCreateView, ParticipantUpdateView, ParticipantDeleteView,
    ProjectParticipantListView, ProjectParticipantDetailView, ProjectParticipantCreateView, ProjectParticipantUpdateView, ProjectParticipantDeleteView
)

urlpatterns = [
    # Participants
    path('', ParticipantListView.as_view(), name='participant_list'),
    path('add/', ParticipantCreateView.as_view(), name='participant_add'),
    path('<int:pk>/', ParticipantDetailView.as_view(), name='participant_detail'),
    path('<int:pk>/edit/', ParticipantUpdateView.as_view(), name='participant_edit'),
    path('<int:pk>/delete/', ParticipantDeleteView.as_view(), name='participant_delete'),

    # Project Participants
    path('project/', ProjectParticipantListView.as_view(), name='projectparticipant_list'),
    path('project/add/', ProjectParticipantCreateView.as_view(), name='projectparticipant_add'),
    path('project/<int:pk>/', ProjectParticipantDetailView.as_view(), name='projectparticipant_detail'),
    path('project/<int:pk>/edit/', ProjectParticipantUpdateView.as_view(), name='projectparticipant_edit'),
    path('project/<int:pk>/delete/', ProjectParticipantDeleteView.as_view(), name='projectparticipant_delete'),
]
