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
from .recommend_post import get_recommendations_post
from operator import itemgetter

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

# === Users ===


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


class Login(View):
    """
    If user logged in with Django authentication. Hardcode and redirect them to the react application Router (Define it later)
    Then give it an argument with the logged in user id for next usage. (It can only be provied within the url though)
    """
    def get(self, request):
        with connection.cursor() as cursor:

            username = request.user
            userid_query = """
                SELECT userid FROM BUser
                WHERE username = %s;
            """
            cursor.execute(userid_query, [username])
            user_id = cursor.fetchone()[0]
            print(user_id)
            return redirect(f"https://backpack-ing.herokuapp.com/?user_id={user_id}")


class FacebookSignup(View):

    def post(self, request):
        """
        Called after a user signs up with facebook in the frontend. The frontend would provide a facebook_user_id
        that is unique for matching whenever they log back in with facebook to be used to retrieve their information
        """
        with connection.cursor() as cursor:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            facebook_user_id = data['user_id']  # How is the frontend going to pass the info in?
            username = data['name']
            email = data['email']  # .....!!!!! About to pass in fb user's email? MUST NEED IN THIS SCHEMA
            profile_pic = data['profile_pic']

            insert_new_facebook_user_query = """
                INSERT INTO BUser (facebook_user_id, username, email, profile_pic)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_new_facebook_user_query, [facebook_user_id, username, email, profile_pic])

            # Initialize the user travel info table
            get_facebook_created_userid_query = """
                                SELECT userid FROM BUser
                                WHERE facebook_user_id = %s;
                            """
            cursor.execute(get_facebook_created_userid_query, [facebook_user_id])
            row = cursor.fetchone()  # row of size one with just the userid

            initialize_user_travelInfo_query = """
                                INSERT INTO Travelinfo (userid) 
                                VALUES (%s);
                            """
            cursor.execute(initialize_user_travelInfo_query, [row[0]])
            return JsonResponse(dict(
                {
                    "Message": "User 'userid ({})' signed up with facebook".format(row[0]),
                    "data": row[0]
                }
            ))


class FacebookLogin(View):
    """
    Called when user logs in with facebook through the frontend. It retrieves the corresponding userid with the
    facebook provided user_id to keep the session info based on this user in our application.
    Returns json data with "userid" of our application userid in the database
    """
    def get(self, request, user_id):
        with connection.cursor() as cursor:
            facebook_user_id = user_id

            get_userid_from_facebook_query = """
                SELECT userid FROM BUser
                WHERE facebook_user_id = %s;
            """
            cursor.execute(get_userid_from_facebook_query, [facebook_user_id])
            row = cursor.fetchone()
            return JsonResponse(dict({
                "data": row[0] if row else None
            }))


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
            user_info_row = cursor.fetchone()  # Tuple containing values of the row (Just values though...)
            print(user_info_row)
            user_info_columns = [col[0] for col in cursor.description]

            fetch_user_travelinfo_query = """
                SELECT * FROM Travelinfo
                WHERE userid = %s;
            """
            cursor.execute(fetch_user_travelinfo_query, [pk])
            user_travel_info_row = cursor.fetchone()
            travel_info_columns = [col[0] for col in cursor.description]

            columns = user_info_columns + travel_info_columns
            row = user_info_row + user_travel_info_row

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
                    {"Message": "ERROR. Title already exists for author '%s'" % author, "data": {}}), status=405)

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
            fetch_post_list_query = """
                SELECT * FROM
                (SELECT * FROM BlogPost P LEFT JOIN
                (SELECT COUNT(*) AS likenum, postid AS pid FROM LikePost GROUP BY postid) T
                ON T.pid = P.postid) T2 LEFT JOIN 
                (SELECT GROUP_CONCAT(tag) AS tags, postid AS pid1 FROM BlogTag GROUP BY postid) T1
                ON T2.postid = T1.pid1;
            """

            cursor.execute(fetch_post_list_query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]

            for elem in dict_ans:
                if elem['likenum'] is None:
                    elem['likenum'] = 0
                if elem['tags'] is None:
                    elem['tags'] = ""
        return JsonResponse(dict_ans, safe=False)


class ListUserComments(View):

    def get(self, request, user_id):
        with connection.cursor() as cursor:
            fetch_user_comment_query = """
            SELECT * FROM Comment
            WHERE userid = %s
            """
            cursor.execute(fetch_user_comment_query, [user_id])
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]
        return JsonResponse(dict_ans, safe=False)


class ListUserLikes(View):

    def get(self, request, user_id):
        with connection.cursor() as cursor:
            fetch_user_likes_query = """
            SELECT * FROM Likepost
            WHERE userid = %s
            """
            cursor.execute(fetch_user_likes_query, [user_id])
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]
        return JsonResponse(dict_ans, safe=False)


class ListPostComments(View):

    def get(self, request, postid):
        with connection.cursor() as cursor:
            fetch_user_list_query = "SELECT * FROM comment WHERE postid = %s;"
            cursor.execute(fetch_user_list_query, [postid])
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]
        return JsonResponse(dict_ans, safe=False)


class ListUserBlogPosts(View):

    def get(self, request, user_id):
        with connection.cursor() as cursor:
            fetch_user_info_query = """
                SELECT * FROM
                (SELECT * FROM (SELECT * FROM BlogPost WHERE author = %s) P LEFT JOIN 
                (SELECT COUNT(*) AS likenum, postid AS pid FROM LikePost GROUP BY postid) T
                ON T.pid = P.postid) T2 LEFT JOIN 
                (SELECT GROUP_CONCAT(tag) AS tags, postid AS pid1 FROM BlogTag GROUP BY postid) T1
                ON T2.postid = T1.pid1;
            """
            cursor.execute(fetch_user_info_query, [user_id])
            rows = cursor.fetchall()  # Tuple containing values of the row (Just values though...)
            columns = [col[0] for col in cursor.description]
            dict_ans = [dict(zip(columns, row)) for row in rows]
            for elem in dict_ans:
                if elem['likenum'] is None:
                    elem['likenum'] = 0
                if elem['tags'] is None:
                    elem['tags'] = ""
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
                    post_id), "data": {}}), status=404
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
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LikeBlogPost, self).dispatch(*args, **kwargs)

    @csrf_exempt
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


class DeleteLikePost(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DeleteLikePost, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request):
        with connection.cursor() as cursor:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            postid = data['postid']
            userid = data['userid']

            fetch_user_info_query = """
                DELETE FROM LikePost
                WHERE postid = %s AND userid = %s
            """
            try:
                cursor.execute(fetch_user_info_query, [postid, userid])
            except:
                return JsonResponse(dict({"Message": "fail to delete like"}), status=500)
        return JsonResponse(dict({"Message": "deleted like"}))


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
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body["content"]
        user_id = body['userid']
        post_id = body['post_id']
        # None would be converted to NULL
        parent_id = body['parent_id'] if body['parent_id'] != "None" else None

        with connection.cursor() as cursor:
            create_comment_query = """
                INSERT INTO comment(content, postid, userid, parentid)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(create_comment_query, [content, post_id, user_id, parent_id])

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

    def get(self, request, comment_id):
        with connection.cursor() as cursor:
            fetch_comment_query = """ 
                SELECT * FROM Comment
                WHERE commentid = %s
            """
            cursor.execute(fetch_comment_query, [comment_id])
            row = cursor.fetchone()
            # print("row", row[4])
            # if row[4] != user_id:
            #     return JsonResponse(dict({"Message": "The current user does not have the permission to update the comment"}))
            columns = [col[0] for col in cursor.description]
            dict_ans = dict(zip(columns, row))
        return JsonResponse(dict_ans, safe=False)

    @csrf_exempt
    def put(self, request, comment_id):
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
    def delete(self, request, comment_id):
        with connection.cursor() as cursor:
            # filter_user_query = """
            #     SELECT userid FROM Comment
            #     WHERE commentid = %s
            # """
            # cursor.execute(filter_user_query, [comment_id])
            # row = cursor.fetchone()
            # if row[0] != user_id:
            #     return JsonResponse(
            #         dict(
            #             {"Message": "The current user does not have the permission to delete the comment"}),
            #         status=405)
            delete_comment_query = """
                DELETE FROM Comment
                WHERE commentid = %s
            """
            cursor.execute(delete_comment_query, [comment_id])
        return JsonResponse(dict({"Message": "deleted comment with comment_id: '%s'" % comment_id}))


class AddBlogTag(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddBlogTag, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request, postid):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        tag = body["tag"]

        with connection.cursor() as cursor:
            create_blogtag_query = """
                        INSERT INTO BlogTag(tag, postid)
                        VALUES (%s, %s);
                    """
            cursor.execute(create_blogtag_query, [tag, postid])

        return JsonResponse(dict({"Message": "OK", "data": body}))


class DeleteBlogTag(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DeleteBlogTag, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request, postid):
        with connection.cursor() as cursor:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            tag = body["tag"]

            fetch_user_info_query = """
                DELETE FROM BlogTag
                WHERE postid = %s AND tag = %s
            """
            try:
                cursor.execute(fetch_user_info_query, [postid, tag])
            except:
                return JsonResponse(dict({"Message": "fail to delete blogtag"}), status=500)
        return JsonResponse(dict({"Message": "deleted blogtag"}))


class ConnectUsers(View):
    def get(self, request, userid):
        with connection.cursor() as cursor:
            fetch_user_likes_query = """
                SELECT author AS likes, COUNT(postid) AS likes_count FROM BlogPost WHERE postid in
                (SELECT postid FROM LikePost WHERE userid = %s) GROUP BY likes;
            """
            cursor.execute(fetch_user_likes_query, [userid])
            likes_rows = cursor.fetchall()  # Tuple containing values of the row (Just values though...)
            likes_columns = [col[0] for col in cursor.description]
            likes_dict = [dict(zip(likes_columns, row)) for row in likes_rows]

            fetch_user_liked_query = """
                SELECT T2.userid AS liked, COUNT(*) AS liked_count FROM
                (SELECT postid FROM BlogPost WHERE author = %s) T1 JOIN
                (SELECT * FROM LikePost) T2 ON T1.postid = T2.postid GROUP BY liked;
            """
            cursor.execute(fetch_user_liked_query, [userid])
            liked_rows = cursor.fetchall()  # Tuple containing values of the row (Just values though...)
            liked_columns = [col[0] for col in cursor.description]
            liked_dict = [dict(zip(liked_columns, row)) for row in liked_rows]

            fetch_user_travel_query = """
                            SELECT destination, budgetMax, budgetMin 
                            FROM Travelinfo WHERE userid = %s;
                        """
            cursor.execute(fetch_user_travel_query, [userid])
            travel_info = cursor.fetchone()

            similar_travel = []
            if travel_info is None:
                pass
            else:
                fetch_similar_travel_query = """
                                SELECT userid as similar_traveller FROM Travelinfo 
                                WHERE destination = %s AND 
                                budgetMax BETWEEN %s AND %s AND
                                budgetMin BETWEEN %s AND %s;
                            """
                cursor.execute(fetch_similar_travel_query, [travel_info[0], travel_info[1] - 200, travel_info[1] + 200,
                                                            travel_info[2] - 200, travel_info[2] + 200])

                travel_rows = cursor.fetchall()
                travel_columns = [col[0] for col in cursor.description]

                similar_travel = [dict(zip(travel_columns, row)) for row in travel_rows]

            fetch_user_comment_query = """
                            SELECT author AS comment_on, COUNT(*) AS commenton_count FROM BlogPost WHERE postid IN 
                            (SELECT postid FROM Comment WHERE userid = %s) GROUP BY comment_on;
                        """
            cursor.execute(fetch_user_comment_query, [userid])
            commenton_rows = cursor.fetchall()
            commenton_columns = [col[0] for col in cursor.description]
            commenton_dict = [dict(zip(commenton_columns, row)) for row in commenton_rows]

            fetch_user_comment_query = """
                            SELECT T2.userid AS comment_from, COUNT(*) AS commentfrom_count FROM
                            (SELECT postid FROM BlogPost WHERE author = %s) T1 JOIN
                            (SELECT * FROM Comment) T2 ON T1.postid = T2.postid GROUP BY comment_from;
                        """
            cursor.execute(fetch_user_comment_query, [userid])
            commentfrom_rows = cursor.fetchall()  # Tuple containing values of the row (Just values though...)
            commentfrom_columns = [col[0] for col in cursor.description]
            commentfrom_dict = [dict(zip(commentfrom_columns, row)) for row in commentfrom_rows]

            relations = {}

            for person in likes_dict:
                try:
                    tmp = relations[person['likes']]
                except:
                    relations[person['likes']] = {}

                try:
                    relations[person['likes']]['likes'] += person['likes_count']
                except:
                    relations[person['likes']]['likes'] = person['likes_count']

            for person in liked_dict:
                try:
                    tmp = relations[person['liked']]
                except:
                    relations[person['liked']] = {}

                try:
                    relations[person['liked']]['liked'] += person['liked_count']
                except:
                    relations[person['liked']]['liked'] = person['liked_count']

            for person in similar_travel:

                try:
                    tmp = relations[person['similar_traveller']]
                except:
                    relations[person['similar_traveller']] = {}

                # try:
                #     relations[person['similar_traveller']] += ',similar_travel'

                relations[person['similar_traveller']]['similar_traveller'] = 1

            for person in commenton_dict:
                try:
                    tmp = relations[person['comment_on']]
                except:
                    relations[person['comment_on']] = {}
                try:
                    relations[person['comment_on']]['comment_on'] += person['commenton_count']
                except:
                    relations[person['comment_on']]['comment_on'] = person['commenton_count']

            for person in commentfrom_dict:
                try:
                    tmp = relations[person['comment_from']]
                except:
                    relations[person['comment_from']] = {}
                try:
                    relations[person['comment_from']]['comment_from'] += person['commentfrom_count']
                except:
                    relations[person['comment_from']]['comment_from'] = person['commentfrom_count']

            del relations[userid]

        # Setting safe to allow JsonResponse to respond with something other than a dictionary (dict()) object
        return JsonResponse(relations, safe=False)


class RecommendPosts(View):
    def get(self, request, user_id):
        with connection.cursor() as cursor:
            fetch_user_likes_query = """
                SELECT postid FROM Likepost
                WHERE userid = %s
            """
            cursor.execute(fetch_user_likes_query, [user_id])
            rows = cursor.fetchall()
            if len(rows) == 0:
                return JsonResponse(dict({"Message": "Current user does not have any like posts, please add posts you like and then we can recommend posts"}), status=500)
            # columns = [col[0] for col in cursor.description]
            # dict_ans = [dict(zip(columns, row)) for row in rows]
            res = {}

            fetch_posts = """
                SELECT * FROM blogpost
            """
            cursor.execute(fetch_posts, [])
            blogs = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            blogdict = [dict(zip(columns, row)) for row in blogs]


            for row in rows:
                postid_list = get_recommendations_post(blogdict, row[0])
                for postid in postid_list:
                    if postid[0] in map(lambda x: x[0], rows):
                        continue
                    if postid[0] in res:
                        res[postid[0]] += postid[1]
                    else:
                        res[postid[0]] = postid[1]

        return JsonResponse(sorted(res.items(), key=itemgetter(1)), safe=False)

