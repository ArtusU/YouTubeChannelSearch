from django.urls import path, include

from .views import index, channel_search, add_channel, generate, get_progress

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('channelsearch/', channel_search, name='channel-search'),
    path('addchannel/<channel_id>/', add_channel, name='add-channel'),
    path('generate/', generate, name='generate'),
    path('get_progress/<task_id>/', get_progress, name='get-progress'),
]