import json
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

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

            cleaned_form_data = form.cleaned_data
            # This thing is unique for django
            username = cleaned_form_data.get('username')
            raw_password = cleaned_form_data.get('password1')
            first_name = cleaned_form_data.get("first_name")
            last_name = cleaned_form_data.get("last_name")
            email = cleaned_form_data.get("email")

            # Save the user info into Mysql Database
            with connection.cursor() as cursor:
                initialize_user_query = """
                    INSERT INTO BUser (open_match, username, firstname, lastname, info, profile_pic, email) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                # """
                #                     INSERT INTO BUser (open_match, nickname, info, profile_pic)
                #                     VALUES (%s, %s, %s, %s);
                #                 """
                cursor.execute(initialize_user_query, [
                               0, username, first_name, last_name, "", "", email])

                get_created_user_query = """
                    SELECT userid FROM BUser
                    WHERE username = %s;
                """
                cursor.execute(get_created_user_query, [username])
                row = cursor.fetchone()  # row of size one with just the userid

                initialize_user_travelInfo_query = """
                    INSERT INTO Travelinfo (userid) 
                    VALUES (%s);
                """
                cursor.execute(initialize_user_travelInfo_query, [row[0]])

            form.save()
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
        # [] Returns a list of TAGS??????!!!

        # Check if post with the same title exists
        with connection.cursor() as cursor:
            get_blog_post_with_title = """
                SELECT COUNT(*) FROM BlogPost
                WHERE title = %s AND author = %s;
            """
            cursor.execute(get_blog_post_with_title, [title, author])
            row = cursor.fetchone()
            print("row", row)

        if row[0] > 0:
            return JsonResponse(
                dict(
                    {"Message": "ERROR. Title already exists for author '%s'" % author, "data": {}})
                , status=405)

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

    def get_object(self, post_id):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM BlogPost
                WHERE postid = %s
            """
            cursor.execute(fetch_user_info_query, [post_id])
            row = cursor.fetchone()
        return row

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
        row = self.get_object(post_id)

        # all updates should be changed like this
        title = body['title'] if 'title' in body else row[1]
        content = body['content'] if 'content' in body else row[2]
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
                ,status=404
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
            print("row", row)
            columns = [col[0] for col in cursor.description]
            updated_blog_post_data = dict(zip(columns, row))

        # Return the updated_values of the updated BlogPost
        return JsonResponse(
            dict({"Message": "updated blogpost with post_id: '%s'" %
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
                return JsonResponse(dict({"Message": "fail to delete blogpost with post_id: '%s'" % post_id}), status=500)
        return JsonResponse(dict({"Message": "deleted blogpost with post_id: '%s'" % post_id}))


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
                return JsonResponse(dict({"Message": "fail to like"}), status=500)
        return JsonResponse(dict({"Message": "like added"}))


# class CreateTravelInfo(View):

#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super(CreateTravelInfo, self).dispatch(*args, **kwargs)

#     def get(self, requestk, user_id):
#         with connection.cursor() as cursor:
#             fetch_user_info_query = """
#                 SELECT * FROM Travelinfo
#                 WHERE userid = %s
#             """
#             cursor.execute(fetch_user_info_query, [user_id])
#             row = cursor.fetchall()

#             columns = [col[0] for col in cursor.description]
#             dict_ans = dict(zip(columns, row))

#         return JsonResponse(dict({"message": dict_ans}))

#     @csrf_exempt
#     def post(self, request, user_id):
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         activity = body["activity"]
#         budgetmax = body["budgetmax"]
#         budgetmin = body["budgetmin"]
#         destination = body["destination"]
#         starttime = body["starttime"]
#         endtime = body["endtime"]

#         with connection.cursor() as cursor:
#             create_travel_info = """
#             INSERT INTO Travelinfo(activity, budgetmax, budgetmin, destination, starttime, endtime, userid)
#             VALUES(%s, %s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(create_travel_info, [
#                 activity, budgetmax, budgetmin, destination, starttime, endtime, user_id])

#         return JsonResponse(dict({"Message": "OK", "data": body}))


class UpdateTravelInfo(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdateTravelInfo, self).dispatch(*args, **kwargs)

    def get_object(self, user_id):
        with connection.cursor() as cursor:
            fetch_user_travelinfo_query = """
                SELECT * FROM Travelinfo
                WHERE userid = %s
            """
            cursor.execute(fetch_user_travelinfo_query, [user_id])
            row = cursor.fetchone()
        return row

    def get(self, request, user_id):
        with connection.cursor() as cursor:
            fetch_user_travelinfo_query = """
                SELECT * FROM Travelinfo
                WHERE userid = %s
            """
            cursor.execute(fetch_user_travelinfo_query, [user_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))
        return JsonResponse(dict_ans, safe=False)

    @csrf_exempt
    def put(self, request, user_id):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        row = self.get_object(user_id)
        activity = body['activity'] if 'activity' in body else row[1]
        budgetmax = body['budgetMax'] if 'budgetMax' in body else row[2]
        budgetmin = body['budgetMin'] if 'budgetMin' in body else row[3]
        destination = body['destination'] if 'destination' in body else row[4]
        starttime = body['starttime'] if 'starttime' in body else row[5]
        endtime = body['endtime'] if 'endtime' in body else row[6]

        with connection.cursor() as cursor:
            update_travel_info_query = """
                Update Travelinfo
                SET activity = %s, budgetmax = %s, budgetmin = %s, destination = %s, starttime = %s, endtime = %s
                WHERE userid = %s
            """
            cursor.execute(update_travel_info_query, [
                           activity, budgetmax, budgetmin, destination, starttime, endtime, user_id])

            # query
            fetch_new_travelinfo_query = """
                SELECT * FROM Travelinfo
                WHERE userid = %s
            """
            cursor.execute(fetch_new_travelinfo_query, [user_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))

        return JsonResponse(dict({
            "Message": "updated travelinfo of use_id: %s" % user_id,
            "data": dict_ans
        }))


# for delete it should also be update to all blank
class DeleteTravelInfo(View):

    def delete(self, request, user_id):
        with connection.cursor() as cursor:
            delete_user_travelinfo_query = """
                Update Travelinfo
                SET activity = '', budgetmax = 0, budgetmin = 0, destination = '', starttime = Null, endtime = Null 
                WHERE userid = %s
            """

            cursor.execute(delete_user_travelinfo_query, [user_id])
        return JsonResponse(dict({"Message": "delete travelinfo of %s successfully" % user_id}))


class CreateComment(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CreateComment, self).dispatch(*args, **kwargs)

    def get(self, request, user_id, parent_id, post_id):
        return JsonResponse(dict({"Message":
                                  "just for test"}))

    @csrf_exempt
    def post(self, request, user_id, parent_id, post_id):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body["content"]

        with connection.cursor() as cursor:
            create_comment_query = """
                INSERT INTO comment(content, postid, userid, parentid)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(create_comment_query, [
                           content, post_id, user_id, parent_id])

            return JsonResponse(dict({"Message": "OK", "data": body}))


class UpdateComment(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdateComment, self).dispatch(*args, **kwargs)

    # if the current user is not the user who create this comment
    # then in get function, we prevent the current user to update
    # so the current user has no chance to execute post function
    # front end should use this get function's info

    def get_object(self, comment_id):
        with connection.cursor() as cursor:
            fetch_comment_query = """ 
                SELECT * FROM Comment
                WHERE commentid = %s
            """
            cursor.execute(fetch_comment_query, [comment_id])
            row = cursor.fetchone()
        return row

    def get(self, request, comment_id, user_id):
        with connection.cursor() as cursor:
            fetch_comment_query = """ 
                SELECT * FROM Comment
                WHERE commentid = %s
            """
            cursor.execute(fetch_comment_query, [comment_id])
            row = cursor.fetchone()
            print("row", row[4])
            if row[4] != user_id:
                return JsonResponse(dict({"Message": "The current user does not have the permission to update the comment"}))
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))
        return JsonResponse(dict_ans, safe=False)

    @csrf_exempt
    def put(self, request, comment_id, user_id):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        row = self.get_object(comment_id)
        content = body['content'] if 'content' in body else row[2]

        with connection.cursor() as cursor:
            update_comment_query = """
                UPDATE Comment
                SET content = %s
                WHERE commentid = %s
            """
            cursor.execute(update_comment_query, [content, comment_id])

            updated_comment_query = """
                SELECT * FROM Comment
                WHERE commentid = %s
            """
            cursor.execute(updated_comment_query, [comment_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))

        return JsonResponse(dict({
            "Message": "updated comment for commentid: %s" % comment_id,
            "data": dict_ans
        }))


class DeleteComment(View):
    def delete(self, request, comment_id, user_id):
        with connection.cursor() as cursor:
            filter_user_query = """
                SELECT userid FROM Comment
                WHERE commentid = %s
            """
            cursor.execute(filter_user_query, [comment_id])
            row = cursor.fetchone()
            if row[0] != user_id:
                return JsonResponse(
                    dict({"Message": "The current user does not have the permission to delete the comment"}),
                        status=405)
            delete_comment_query = """
                DELETE FROM Comment
                WHERE commentid = %s
            """
            cursor.execute(delete_comment_query, [comment_id])
        return JsonResponse(dict({"Message": "deleted comment with comment_id: '%s'" % comment_id}))
