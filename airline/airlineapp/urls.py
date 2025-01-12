from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_filter, name='flight_filter'),
    path('results/', views.index, name='flight_results'),  # Separate path for the results page
    path('admin/', views.admin, name='admin'),
]
