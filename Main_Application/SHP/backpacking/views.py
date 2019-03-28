from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from django.db import connection



"""
actions: (High level queries/posts/updates CRUD)
1. User related:
    1. Get all users historical posts |
    2. Get user information
    3. Get user commnets
    4. Get user's liked posts (following)
    5. Get user's historical travel info
    6. Get user's info on being open to travel
2. Posts:
    1. Creator info
    2. Commented user info
    3. liked user info
    4. posted time
    5. posts info
    6. post tags / posts with same tags (overlapping ?)
    
"""


class UserList(View):

    def get(self, request):
        with connection.cursor() as cursor:
            fetch_user_list_query = "SELECT * FROM BUser"
            cursor.execute(fetch_user_list_query)
            rows = cursor.fetchall()
            print(rows)

            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]
            print(dict_ans)
            print(cursor.description)
        return JsonResponse(dict_ans, safe=False)
        # return row


class UserInfo(View):

    def get(self, request, pk):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM BUser
                WHERE userid = %s
            """
            cursor.execute(fetch_user_info_query, [pk])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))
        return JsonResponse(dict_ans, safe=False)  # Setting safe to allow JsonResponse to respond with something other than a dictionary (dict()) object


class CreateBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    def get(self, request):
        return JsonResponse(dict({"say":
    "Created with GET cause I'm just useless at the moment since no one told me what method they will use on me...."}))

    def post(self, request):
        return JsonResponse(dict({"say":"Created with post"}))


class ListBlogPosts(View):

    def get(self, request):
        return JsonResponse(dict({"status": "Listing all blog posts"}))


class ListUserBlogPosts(View):

    def get(self, request, user_id):
        return JsonResponse(dict({"status": "Listing all blog posts for user_id: '%s'" % user_id}))


class UpdateBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    def get(self, request, post_id):
        return JsonResponse(dict({"say":
    "Created with GET cause I'm just useless at the moment since no one told me what method they will use on me...."}))

    def post(self, request, post_id):
        return JsonResponse(dict({"status": "updated blogpost with post_id: '%s'" % post_id}))


class DeleteBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    def get(self, request, post_id):
        return JsonResponse(dict({"say":
    "Created with GET cause I'm just useless at the moment since no one told me what method they will use on me...."}))

    def post(self, request, post_id):
        return JsonResponse(dict({"status": "updated blogpost with post_id: '%s'" % post_id}))


class SearchBlogPost(View):
    # Content or title
    def get(self, request, search_keyword):
        return JsonResponse(dict({"status": "Got blogpost based on search_keyword: '%s'" % search_keyword}))


class LikeBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    def get(self, request):
        return JsonResponse(dict({"say":
    "Created with GET cause I'm just useless at the moment since no one told me what method they will use on me...."}))

    def post(self):
        return JsonResponse(dict({"status": "blablbalblabalalblablablablabla"}))



