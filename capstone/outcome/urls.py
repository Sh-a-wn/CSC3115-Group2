from django.urls import path
from .views import (
    OutcomeListForProjectView,
    OutcomeDetailView,
    OutcomeCreateView,
    OutcomeUpdateView,
    OutcomeDeleteView,
)

urlpatterns = [
    path("project/<int:project_id>/", OutcomeListForProjectView.as_view(), name="project_outcomes"),
    path("project/<int:project_id>/add/", OutcomeCreateView.as_view(), name="outcome_add_for_project"),

    path("<int:pk>/", OutcomeDetailView.as_view(), name="outcome_detail"),
    path("<int:pk>/edit/", OutcomeUpdateView.as_view(), name="outcome_edit"),
    path("<int:pk>/delete/", OutcomeDeleteView.as_view(), name="outcome_delete"),
]