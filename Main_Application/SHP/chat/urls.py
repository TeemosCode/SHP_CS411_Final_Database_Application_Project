from django.urls import path, re_path
from .views import index, room, PrivateChat


app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('privateChat/', PrivateChat.as_view(), name='private_chat_urlpattern'),
    re_path(r'^chatroom/(?P<room_name>[^/]+)/$', room, name='room'),

]
