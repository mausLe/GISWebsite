from django.shortcuts import render
from django.http import HttpResponse

import os, folium

# Create your views here.
def createMap():
    m = folium.Map(location = [10.869800, 106.803000], zoom_start = 20)

    m = m._repr_html_()
    context = {"my_map": m}

    return context

def home(request):
    context = createMap()

    return render( request, "accounts/main.html", context)

def location(request):

    # read real time data
    context = createMap()

    return render( request, "accounts/location.html", context)


def history(request):
    # Load database to mark user location

    return render( request, "accounts/history.html")
