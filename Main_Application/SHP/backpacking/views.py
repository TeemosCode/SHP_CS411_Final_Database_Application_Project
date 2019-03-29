# from django.core.serializers import json
import json
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse, HttpResponse
import json

from django.db import connection


from django.views.decorators.csrf import csrf_exempt # !!!!!

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
    """Get the total list of current users"""
    def get(self, request):
        with connection.cursor() as cursor:
            fetch_user_list_query = "SELECT * FROM BUser;"
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
    """Get each individual user information based on user ID"""
    def get(self, request, pk):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM BUser
                WHERE userid = %s;
            """
            cursor.execute(fetch_user_info_query, [pk])
            row = cursor.fetchone()  # Tuple containing values of the row (Just values though...)
            print(row)
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))
        return JsonResponse(dict_ans, safe=False)  # Setting safe to allow JsonResponse to respond with something other than a dictionary (dict()) object


class CreateBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    """Source: https://stackoverflow.com/questions/41709347/django-csrf-exempt-not-working-in-class-view/41728627"""
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CreateBlogPost, self).dispatch(*args, **kwargs)

    def get(self, request):
        return JsonResponse(dict({"say":
    "Created with GET cause I'm just useless at the moment since no one told me what method they will use on me...."}))

    @csrf_exempt
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)  # Creates python dicts
        title = body['title']  # Access these data one by one
        content = body['content']
        author = body['author']

        # Check if post with the same title exists
        with connection.cursor() as cursor:
            get_blog_post_with_title = """
                SELECT COUNT(*) FROM BlogPost
                WHERE title = %s AND author = %s;
            """
            cursor.execute(get_blog_post_with_title, [title, author])
            row = cursor.fetchone()
            if row[0] > 0:
                return JsonResponse(dict({"Message": "ERROR. Title already exists for author '%s'" % author, "data": {}}))

        # If post title name is not duplicate for the author, create the new post
        with connection.cursor() as cursor:
            insert_new_blog_post = """
                INSERT INTO BlogPost (title, content, author)
                VALUES (%s, %s, %s);
            """
            cursor.execute(insert_new_blog_post, [title, content, author])

        return JsonResponse(dict({"Message": "OK", "data": body}))


class ListBlogPosts(View):

    def get(self, request):
        return JsonResponse(dict({"status": "Listing all blog posts"}))


class ListUserBlogPosts(View):

    def get(self, request, user_id):
        return JsonResponse(dict({"status": "Listing all blog posts for user_id: '%s'" % user_id}))


class UpdateBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    def get(self, request, post_id):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM BlogPost
                WHERE postid = %s
            """
            cursor.execute(fetch_user_info_query, [post_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))
        return JsonResponse(dict_ans, safe=False)

    #     return JsonResponse(dict({"say":
    # "Created with GET cause I'm just useless at the moment since no one told me what method they will use on me...."}))

    def post(self, request, post_id):
        body = request.body.decode('utf-8')
        data = json.loads(body)
        title = data['title']
        content = data['content']
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                UPDATE BlogPost SET title = %s, content = %s
                WHERE postid = %s
            """
            try:
                cursor.execute(fetch_user_info_query, [title, content, post_id])
            except:
                return JsonResponse(dict({"status": "fail to update blogpost with post_id: '%s'" % post_id}))
        return JsonResponse(dict({"status": "updated blogpost with post_id: '%s'" % post_id}))


class DeleteBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    def get(self, request, post_id):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM BlogPost
                WHERE postid = %s
            """
            cursor.execute(fetch_user_info_query, [post_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))
        return JsonResponse(dict_ans, safe=False)

    def post(self, request, post_id):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                DELETE FROM BlogPost
                WHERE postid = %s
            """
            try:
                cursor.execute(fetch_user_info_query, [post_id])
            except:
                return JsonResponse(dict({"status": "fail to delete blogpost with post_id: '%s'" % post_id}))
        return JsonResponse(dict({"status": "deleted blogpost with post_id: '%s'" % post_id}))


class SearchBlogPost(View):
    # Content or title
    def get(self, request, search_keyword):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM BlogPost
                WHERE %s IN title OR %s IN content
            """
            cursor.execute(fetch_user_info_query, [search_keyword])
            rows = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]

        return JsonResponse(dict_ans, safe=False)


class LikeBlogPost(View):
    ### No use at the moment since post or get is defined by the events happening on the client side
    # def get(self, request):
    #
    #     return JsonResponse(dict({"say":
    # "Created with GET cause I'm just useless at the moment since no one told me what method they will use on me...."}))

    def post(self, request):
        with connection.cursor() as cursor:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            postid = data['postid']
            userid = data['userid']

            fetch_user_info_query = """
                INSERT INTO LikePost (postid, userid)
                VALUES (%s, %s)
            """
            try:
                cursor.execute(fetch_user_info_query, [postid, userid])
            except:
                return JsonResponse(dict({"status": "fail to like"}))
        return JsonResponse(dict({"status": "like added"}))



