import requests, json
from django.http import HttpResponse
from django.shortcuts import render

def upload_file(file):
    url = "http://127.0.0.1:5000/video"
    requests.post(url, file)
    return render(request, 'panel/upload.html', {'response': "Envoyé"}))

upload_file(video)