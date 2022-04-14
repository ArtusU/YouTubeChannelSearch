from django.shortcuts import render

# Create your views here.
from .models import Channel, Video, Channel



def index(request):
    context = {}
    return render(request, 'index.html', context)