from unittest import result
import requests
from celery.result import AsyncResult
from celery_progress.backend import Progress
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from .models import Channel, Video, Channel
from django.views.decorators.csrf import csrf_exempt
from .tasks import get_video_stats


def index(request):
    channels = Channel.objects.all()
    results = Video.objects.order_by('-views')[0:50]

    context = {'channels': channels, 'results': results}
    return render(request, 'index.html', context)


def channel_search(request):
    query = request.GET.get('q')
    url = f'https://www.googleapis.com/youtube/v3/search?q={query}&type=channel&part=snippet&key={settings.YOUTUBE_API_KEY}'
    response = requests.get(url)
    results = response.json()['items']
    context = {'results': results}
    return render(request, 'partials/channel_search_results.html', context=context)


@csrf_exempt
def add_channel(request, channel_id):
    url = f'https://www.googleapis.com/youtube/v3/channels?id={channel_id}&part=snippet,contentDetails&key={settings.YOUTUBE_API_KEY}'
    response = requests.get(url)
    result = response.json()['items'][0]
    
    channel = Channel(
        name=result['snippet']['title'],
        playlist_id=result['contentDetails']['relatedPlaylists']['uploads'],
        thumbnail_url=result['snippet']['thumbnails']['default']['url'],
        description=result['snippet']['description']
        )
    channel.save()
    
    channels = Channel.objects.all()
    context = {'channels': channels}
    return render(request, 'partials/channels.html', context)


def generate(request):
    task = get_video_stats.delay()
    context = {'task_id': task.task_id, 'value': 0}
    return render(request, 'partials/progress_bar.html', context)


def get_progress(request, task_id):
    progress = Progress(AsyncResult(task_id))
    percent_complete = int(progress.get_info()['progress']['percent'])

    if percent_complete == 100:
        results = Video.objects.order_by('-views')[0:50]
        context = {'results': results}
        return render(request, 'partials/results.html', context)
    context = {'task_id': task_id, 'value': percent_complete}
    return render(request, 'partials/progress_bar.html', context)


def get_next_rows(request):
    offset = int(request.GET['offset'])
    results = Video.objects.order_by('-views')[offset:offset+50]
    context = {'results': results, 'offset': offset+50}
    return render(request, 'partials/result_rows.html', context)



