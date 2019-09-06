from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests, json
from forms.forms import UploadForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


# Create your views here.
def test(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue Statfive !</h1>
        <p>Les stats comme sur FIFA !</p>
    """)


@login_required(login_url="/user/login")
def login(request):
    return render(request, 'panel/login.html', {'data': 'Register pour un Five'})


@login_required(login_url="/user/login")
def panel(request):
    return render(request, 'panel/panel.html', {'data': 'Bonjour'})


@login_required(login_url="/user/login")
def upload(request):
    response = ""
    url = "http://127.0.0.1:5000/video"
    if request.method == 'POST':
        if request.FILES['video'] and request.POST['teamA'] and request.POST['teamB']:
            video = request.FILES['video']
            teamA =  request.POST['teamA']
            teamB =  request.POST['teamB']
            data = {'video': video,'teamA':teamA, 'teamB': teamB}
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            print()
            print(video)
            print(data)
            print()
            requests.post(url,files=video, data= data, headers=headers)
            response = "Le fichier a été upload"
            return render(request, 'panel/upload.html', {'data': response})
        else:
            response = "Rien de posté"   
    return render(request, 'panel/upload.html', {'data': response})
