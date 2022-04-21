from django.urls import path, include

from .views import index, channel_search, add_channel

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('channelsearch/', channel_search, name='channel-search'),
    path('addchannel/<channel_id>/', add_channel, name='add-channel'),
]