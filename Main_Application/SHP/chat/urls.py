from django.urls import path, re_path
from .views import index, room, PrivateChat


app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('privateChat/', PrivateChat.as_view(), name='private_chat_urlpattern'),
    path('privateChat/<int:sender_id>/<int:sendto_id>/', PrivateChat.as_view(), name='private_chat_urlpattern'),
    # re_path(r'^chatroom/(?P<room_name>[^/]+)/$', room, name='room'),
    re_path(r'^chatroom/(?P<room_name>[^/]+)/$', PrivateChat.as_view(), name='room'),
]
