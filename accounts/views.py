from builtins import float

from django.shortcuts import render
from django.http import HttpResponse

import os, folium
import turtle
import numpy as np

### ---------------------- Connect 2nd server ------------------
import pymysql
import mysql.connector
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser

#home = expanduser('~')
#mypkey = paramiko.RSAKey.from_private_key_file("C:/RSAkey/test.pem")
# if you want to use ssh password use - ssh_password='your ssh password', bellow

sql_hostname = '127.0.0.1'
sql_username = 'root'
sql_password = 'Admin1234@@'
sql_main_database = 'pets'
sql_port = 3306
ssh_host = '23.99.115.137'
ssh_user = 'thanhhuy98'
ssh_port = 22
sql_ip = '10.0.0.4'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username = ssh_user,
        #ssh_pkey=mypkey,
        ssh_password = 'thanhhuy98',
        remote_bind_address = (sql_hostname, sql_port)) as tunnel:
    # conn = pymysql.connect(host='127.0.0.1', user=sql_username,
    #       passwd=sql_password, db=sql_main_database,
    #      port=tunnel.local_bind_port)

    conn = mysql.connector.connect(
        user = sql_username,
        password = sql_password,
        host = '127.0.0.1',
        port = tunnel.local_bind_port,
        database = sql_main_database,
    )
    mycursor = conn.cursor()
    query = ''' SELECT DISTINCT Longitude FROM TRACKINGDATA WHERE Time > '15:45:00' AND Time <'15:46:00';'''
    query2 = '' 'SELECT * FROM TRACKINGDATA' ''
    mycursor.execute(query2)

    results = mycursor.fetchall()

    numpy_array = np.array(results)
    # trans = numpy_array.transpose()
    # results = trans.tolist()

"""
    new_coord[:, 0] = coord[:, 0]//1000000 + coord[:, 0]%1000000/1000000
    new_coord[:, 1] = coord[:, 1]//1000000 + coord[:, 1]%1000000/1000000
"""

my_coord = []
for item in numpy_array:
    a = item[2]/1000000
    b = item[3]/1000000

    my_coord.append([b, a])
### --------------------------------------------------------------------

# Create your views here.
def createMap():
    m = folium.Map(
        location = [10.869800, 106.803000],
        zoom_start = 20)
    
    coordinates=[(10.869372, 106.802441),(10.870220, 106.802323),(10.870531, 106.802017),(10.871734, 106.802795),(10.873451, 106.802814)]
    coordinates = my_coord
    #a = [float(i) for i in results[2]]
    #b = [float(i) for i in results[3]]
    #coordinates = np.array(a/1000000, b/1000000)
    #coordinates = (float(results[2])/1000000, float(results[3])/1000000)
    for i in range(len(coordinates)):
        t = results[i][4].strftime('%d/%m/%y')
        seconds = results[i][5].total_seconds()
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        h = "%d:%02d:%02d" % (hour, minutes, seconds)
        folium.Marker(location = coordinates[i],
                      icon=folium.Icon(icon="globe")
                      ).add_to(m)

        #folium.Marker(location = coordinates[1],
        #             popup="My first location",
        #             icon=folium.Icon(icon="globe")
        #             ).add_to(m)

    #for each in coordinates:
    #   folium.Marker(each).add_to(m)

    folium.PolyLine(coordinates, color="red", weight=2.5, opacity=1).add_to(m)

    m = m._repr_html_()
    context = {"my_map": m}

    return context

def home(request):

    return location(request)



def location(request):

    # read real time data
    context = createMap()

    return render( request, "accounts/location.html", context)


def history(request):
    # Load database to mark user location
    context = createMap()

    # return render( request, "accounts/history.html", context)
    return render( request, "accounts/navbar.html", context)

