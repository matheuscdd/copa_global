from django.urls import path
from .views import TeamViewAll, TeamViewSpecific

urlpatterns = [
    path('teams/', TeamViewAll.as_view()),
    path('teams/<int:pk>/', TeamViewSpecific.as_view())
]