from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests, json

# Create your views here.

def team(request):
    response = requests.get('http://127.0.0.1:5000/teams/average')
    data = response.json()
    return render(request, 'blog/team.html', {
        'data':data
        })

def match(request):
    response = requests.get('http://127.0.0.1:5000/matchs')
    matchs = response.json()
    return render(request, 'blog/match.html', { 
        'matchs' : matchs
        })
