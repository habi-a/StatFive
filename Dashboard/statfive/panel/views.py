from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests, json
from forms.forms import UploadForm

# Create your views here.
def test(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue Statfive !</h1>
        <p>Les stats comme sur FIFA !</p>
    """)

def login(request):
    return render(request, 'panel/login.html', {'data': 'Register pour un Five'})


def panel(request):
    return render(request, 'panel/panel.html', {'data': 'Bonjour'})

def upload(request):
    response = ""
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        url = "http://127.0.0.1:5000/video"
        requests.post(url, video)
        print(request.FILES['video'])
        response = "Le fichier a été upload"
        return render(request, 'panel/upload.html', {'data': response})
    else:
        response = "Rien de posté"   
    return render(request, 'panel/upload.html', {'data': response})
