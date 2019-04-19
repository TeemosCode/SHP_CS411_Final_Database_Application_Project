from django.urls import path, re_path
from .views import index, room, chatroomyo


app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('chatroomyo/', chatroomyo, name='chatroomyo'),
    re_path(r'^chatroom/(?P<room_name>[^/]+)/$', room, name='room'),

]
