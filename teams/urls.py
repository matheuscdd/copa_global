from django.urls import path
from .views import TeamViewAll

urlpatterns = [
    path('teams/', TeamViewAll.as_view())
]