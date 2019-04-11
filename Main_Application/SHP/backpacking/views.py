from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse, HttpResponse
import json

from django.db import connection

from django.views.decorators.csrf import csrf_exempt  # !!!!!

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


class Home(View):

    def get(self, request):
        return render(request, 'backpacking/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user info into Mysql Database


            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(f"User {username} signed up!")
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('home_urlpattern')
    else:
        form = SignUpForm()
    return render(request, 'backpacking/sign_up.html', {'form': form})


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
        # Setting safe to allow JsonResponse to respond with something other than a dictionary (dict()) object
        return JsonResponse(dict_ans, safe=False)


class CreateBlogPost(View):
    # No use at the moment since post or get is defined by the events happening on the client side
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
        date = body['create_time']
         # [] Returns a list of TAGS??????!!!

        # Check if post with the same title exists
        with connection.cursor() as cursor:
            get_blog_post_with_title = """
                SELECT COUNT(*) FROM BlogPost
                WHERE title = %s AND author = %s;
            """
            cursor.execute(get_blog_post_with_title, [title, author])
            row = cursor.fetchone()

        if row[0] > 0:
            return JsonResponse(
                dict(
                    {"Message": "ERROR. Title already exists for author '%s'" % author, "data": {}})
            )

        # If post title name is not duplicate for the author, create the new post
        with connection.cursor() as cursor:
            insert_new_blog_post = """
                INSERT INTO BlogPost (title, content, author, create_time)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_new_blog_post, [title, content, author, date])

        return JsonResponse(dict({"Message": "OK", "data": body}))


class ListBlogPosts(View):

    def get(self, request):
        with connection.cursor() as cursor:
            fetch_user_list_query = "SELECT * FROM BlogPost;"
            cursor.execute(fetch_user_list_query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]
        return JsonResponse(dict_ans, safe=False)


class ListUserBlogPosts(View):

    def get(self, request, user_id):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM BlogPost
                WHERE author = %s;
            """
            cursor.execute(fetch_user_info_query, [user_id])
            rows = cursor.fetchall()  # Tuple containing values of the row (Just values though...)
            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]
        # Setting safe to allow JsonResponse to respond with something other than a dictionary (dict()) object
        return JsonResponse(dict_ans, safe=False)


class UpdateBlogPost(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdateBlogPost, self).dispatch(*args, **kwargs)

    # No use at the moment since post or get is defined by the events happening on the client side
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

    @csrf_exempt
    def put(self, request, post_id):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)  # Creates python dicts
        title = body['title']  # Access these data one by one
        content = body['content']
        # author = body['author']

        # Check if post with the same post_id exists. If not cannot update.
        with connection.cursor() as cursor:
            get_blog_post_with_postid = """
                SELECT COUNT(*) FROM BlogPost
                WHERE postid = %s;
            """
            cursor.execute(get_blog_post_with_postid, [post_id])
            row = cursor.fetchone()

        if row[0] == 0:
            return JsonResponse(
                dict({"Message": "ERROR. No Post with post_id {%s} exists" % (
                    post_id), "data": {}})
            )

        with connection.cursor() as cursor:
            update_blog_post_with_post_id = """
                UPDATE BlogPost
                SET title = %s, content = %s
                WHERE postid = %s;
            """
            cursor.execute(update_blog_post_with_post_id, [
                           title, content, post_id])

            # Query the updated blogpost data
            query_updated_post_with_post_id = """
                SELECT * FROM BlogPost
                WHERE postid = %s;
            """
            cursor.execute(query_updated_post_with_post_id, [post_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            updated_blog_post_data = dict(zip(columns, row))

        # Return the updated_values of the updated BlogPost
        return JsonResponse(
            dict({"status": "updated blogpost with post_id: '%s'" %
                  post_id, "data": updated_blog_post_data})
            # dict({"status": "updated blogpost with post_id: '%s'" % post_id})
        )


class DeleteBlogPost(View):
    # No use at the moment since post or get is defined by the events happening on the client side
    # def get(self, request, post_id):
    #     with connection.cursor() as cursor:
    #         fetch_user_info_query = """
    #             SELECT * FROM BlogPost
    #             WHERE postid = %s
    #         """
    #         cursor.execute(fetch_user_info_query, [post_id])
    #         row = cursor.fetchone()
    #         columns = [col[0] for col in cursor.description]
    #         dict_ans = dict(zip(columns, row))
    #     return JsonResponse(dict_ans, safe=False)

    def delete(self, request, post_id):
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
    # No use at the moment since post or get is defined by the events happening on the client side
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
