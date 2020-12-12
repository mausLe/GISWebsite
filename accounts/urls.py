from django.urls import path, include
from . import views

urlpatterns = [
    # path("polls/", include("polls.urls")),
    path('', views.home),
    path('location/', views.location),
    path('speed/', views.speed),


]