from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_filter, name='flight_filter'),
    path('results/<int:passenger_id>/', views.index, name='index'),
    path('results/', views.index, name='flight_results'),  # Separate path for the results page
    path('admin/', views.admin, name='admin'),
    path('<int:flight_id>', views.flight, name="flight"),
    path('<int:flight_id>/book', views.book, name="book"),
    path('<int:passenger_id>/deposit', views.deposit, name='deposit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
