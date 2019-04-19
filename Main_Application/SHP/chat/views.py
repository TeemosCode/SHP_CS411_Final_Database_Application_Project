from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from django.views import View
from django.db import connection


def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })


def chatroomyo(request):
    return HttpResponse("Hello WOrld!!")


class PrivateChat(View):

    """
    RuntimeError: You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set. Django can't redirect to the slash URL while maintaining POST data. Change your form to point to 127.0.0.1:8000/chat/privateChat/ (note the trailing slash), or set APPEND_SLASH=False in your Django settings.
HTTP POST /chat/privateChat 500 [0.05, 127.0.0.1:59802]
??!!!!!!!
    """


    def post(self, request):
        # with connection.cursor() as cursor:
        #     body = request.body.decode('utf-8')
        #     data = json.loads(body)
        #     user_id = data['send_from']  # The dude who initiates the chat
        #     send_to_user_id = data['send_to']  # The dude who receives the chat messages
        #
        #     get_userid_from_facebook_query = """
        #         SELECT userid FROM BUser
        #         WHERE facebook_user_id = %s;
        #     """
        #     cursor.execute(get_userid_from_facebook_query, [facebook_user_id])
        #     row = cursor.fetchone()
        #     return JsonResponse(dict({
        #         "data": row[0]
        #     }))
        body = request.body.decode('utf-8')
        data = json.loads(body)
        user_id = data['send_from']  # the one who initiated this chat
        send_to_user_id = data['send_to']
        # first of, need to create the chatroomID based on both user's ID and for linking to private room url using it.
        # Get both user's id, sort them in a list, then concatenate into a string.
        user_id_list = sorted([user_id, send_to_user_id])
        chatroom_id = str(user_id_list[0]) + str(user_id_list[1])
        # Then first check if this chatroom_id already existed, if not insert (create), if yes, then do nothing.
        with connection.cursor() as cursor:
            check_room_id_query = """
                SELECT * FROM PrivateChatRoom
                WHERE chatroomid = %s;
            """
            cursor.execute(check_room_id_query, [chatroom_id])
            row = cursor.fetchone()
            if not row:  # Does NOT exist yet. first time chatting, create the chatroom
                create_new_chatroom_query = """
                    INSERT INTO PrivateChatRoom (chatroomid, member1id, member2id)
                    VALUES (%s, %s, %s); 
                """
                cursor.execute(create_new_chatroom_query, [chatroom_id, user_id_list[0], user_id_list[1]])

            get_user_id_info_query = """
                SELECT * FROM BUser WHERE userid = %s;
            """
            cursor.execute(get_user_id_info_query, [user_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            user_data_dict = dict(zip(columns, row))


        content = {
            'room_name_json': mark_safe(chatroom_id),
            'chatroom_id': mark_safe(chatroom_id),
            'username': mark_safe(user_data_dict['username']),
            'user_fb_img': user_data_dict['profile_pic']
        }
        print(user_id, send_to_user_id)

        # return HttpResponse("Hello WOrld!!")
        return render(request, 'chat/room1.html', content)