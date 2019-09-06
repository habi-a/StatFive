from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests, json
from django.contrib.auth.decorators import login_required


@login_required(login_url="/user/login")
def team(request):
    response = requests.get('http://127.0.0.1:5000/teams/average')
    data = response.json()
    return render(request, 'blog/team.html', {
        'data':data
        })


@login_required(login_url="/user/login")
def match(request):
    response = requests.get('http://127.0.0.1:5000/matchs')
    matchs = response.json()
    return render(request, 'blog/match.html', { 
        'matchs' : matchs
        })


@login_required(login_url="/user/login")
def matchById(request, id):
        url = "http://127.0.0.1:5000/match/" + str(id)
        response = requests.get(url)
        matchs = response.json()
        return render(request, 'blog/detail.html', { 
        'matchs' : matchs
        })
