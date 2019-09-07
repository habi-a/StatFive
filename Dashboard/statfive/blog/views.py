from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests, json

# Create your views here.
def home(request):
    return render(request, 'blog/home.html', {
        'data':'lol'
        })

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

def matchById(request, id):
        url = "http://127.0.0.1:5000/match/" + str(id)
        response = requests.get(url)
        matchs = response.json()
        return render(request, 'blog/detail.html', { 
        'matchs' : matchs
        })

def search(request):
    if request.method == 'GET':
        if request.GET['id']:
                url = "http://127.0.0.1:5000/match/" + request.GET['id']
                response = requests.get(url)
                matchs = response.json()
                return render(request, 'blog/detail.html', { 
                'matchs' : matchs
                })

                