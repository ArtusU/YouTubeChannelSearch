from django.urls import path, include

from .views import index, channel_search

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('channelsearch/', channel_search, name='channel-search')
]