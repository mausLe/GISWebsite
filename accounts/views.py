from django.shortcuts import render
from django.http import HttpResponse

import os, folium
import turtle
import pandas as pd


import time, threading # Use these lib to create periodic Task every 1 sec
WAIT_SECONDS = 1


# Create your views here.
def createMap():
    m = folium.Map(location = [10.869800, 106.803000], zoom_start = 20)

    return m



def home(request):
    
    return location(request)



def location(request):

    # read real time data
    map = createMap()
    
    folium.Marker(location = [10.869800, 106.803000], 
    popup="My location",
    icon=folium.Icon(icon="globe")
    ).add_to(map)

    map = map._repr_html_()
    context = {"my_map": map}

    # threading.Timer(WAIT_SECONDS, location(request)).start()

    return render( request, "accounts/location.html", context)


def history(request):
    # Load database to mark user location
    df = pd.read_csv("accounts\TRACKINGDATA.csv")
    # Swap "Long" vs "Lat" column
    new_column = ["Device_ID", "Long", "Lat", "Date", "Time"]
    new_df = df.reindex(columns=new_column)
    coord = new_df.loc[:10, "Long":"Lat"].values
    new_coord = coord
    new_coord[:, 0] = coord[:, 0]//1000000 + coord[:, 0]%1000000/1000000
    new_coord[:, 1] = coord[:, 1]//1000000 + coord[:, 1]%1000000/1000000

    map = createMap()
    c = [[ 10.869800, 106.803000], [ 10.879830, 106.805000],[ 10.869800, 106.805000]]

    folium.Marker(c[0], popup="Starting point", icon=folium.Icon(color="green", icon="star")).add_to(map)
    folium.Marker(c[-1], popup="Destination", icon=folium.Icon(color="red", icon="globe")).add_to(map)


    # Start marker

    # Create CircleMarker on route
    for item in c:
        folium.CircleMarker(item, radius=7).add_to(map)

    folium.PolyLine(c, color="red", weight=4, opacity=1).add_to(map)

    map = map._repr_html_()
    context = {"my_map": map}

    # return render( request, "accounts/history.html", context)
    return render( request, "accounts/navbar.html", context)

