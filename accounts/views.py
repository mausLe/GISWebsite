from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render( request, "accounts/dashboard.html")

def location(request):
    return render( request, "accounts/location.html")


def speed(request):
    return render( request, "accounts/speed.html")