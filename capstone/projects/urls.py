from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectsByFacilityView,
    ProjectsByProgramView,
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("add/", ProjectCreateView.as_view(), name="project_add"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),

    # Filters
    path("facility/<int:facility_id>/", ProjectsByFacilityView.as_view(), name="projects_by_facility"),
    path("program/<int:program_id>/", ProjectsByProgramView.as_view(), name="projects_by_program"),
]