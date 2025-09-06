from django.urls import path
from .views import (
    OutcomeListForProjectView,
    OutcomeDetailView,
    OutcomeCreateView,
    OutcomeUpdateView,
    OutcomeDeleteView,
)

urlpatterns = [
    path("project/<int:project_id>/outcomes/", OutcomeListForProjectView.as_view(), name="project_outcomes"),
    path("project/<int:project_id>/outcomes/add/", OutcomeCreateView.as_view(), name="outcome_add"),

    path("<int:pk>/", OutcomeDetailView.as_view(), name="outcome_detail"),
    path("<int:pk>/edit/", OutcomeUpdateView.as_view(), name="outcome_edit"),
    path("<int:pk>/delete/", OutcomeDeleteView.as_view(), name="outcome_delete"),
]