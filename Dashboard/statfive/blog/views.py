from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests, json

# Create your views here.

def team(request):
    response = requests.get('http://163.5.245.188:5000/teams/average')
    data = response.json()
    return render(request, 'blog/team.html', {
        'data':data
        })

def match(request):
    response = requests.get('http://163.5.245.188:5000/matchs')
    matchs = response.json()
    return render(request, 'blog/match.html', {
        'matchs' : matchs
        })

def matchById(request, id):
        url = "http://163.5.245.188:5000/match/" + str(id)
        response = requests.get(url)
        matchs = response.json()
        return render(request, 'blog/detail.html', {
        'matchs' : matchs
        })
