from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login1', views.login_view, name="login1"),
    path('logout1', views.logout_view, name="logout1"),
]