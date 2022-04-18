import requests
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from .models import Channel, Video, Channel



def index(request):
    channels = Channel.objects.all()
    context = {'channels': channels}
    return render(request, 'index.html', context)


def channel_search(request):
    query = request.GET.get('q')
    url = f'https://www.googleapis.com/youtube/v3/search?q={query}&type=channel&part=snippet&key={settings.YOUTUBE_API_KEY}'
    response = requests.get(url)
    results = response.json()['items']
    context = {'results': results}
    return render(request, 'partials/channel_search_results.html', context=context)