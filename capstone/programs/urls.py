from django.urls import path
from .views import *

urlpatterns = [
    path('', ProgramListView.as_view(), name='program_list'),
    path('add/', ProgramCreateView.as_view(), name='program_add'),
    path('<int:pk>/', ProgramDetailView.as_view(), name='program_detail'),
    path('<int:pk>/edit/', ProgramUpdateView.as_view(), name='program_edit'),
    path('<int:pk>/delete/', ProgramDeleteView.as_view(), name='program_delete'),
]