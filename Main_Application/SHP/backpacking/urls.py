from django.urls import path
from .views import (
    UserList,
    UserInfo,
    CreateBlogPost,
    UpdateBlogPost,
    DeleteBlogPost,
    LikeBlogPost,
    ListBlogPosts,
    SearchBlogPost,
    ListUserBlogPosts,
    # CreateTravelInfo,
    UpdateTravelInfo,
    CreateComment,
    UpdateComment,
)

urlpatterns = [
    # Path for users
    path('users/list/', UserList.as_view(), name="user_list_urlpattern"),
    path('users/<int:pk>', UserInfo.as_view(), name="user_info_urlpattern"),
    # Path for blogpost
<<<<<<< Updated upstream
    path('blogpost/create/', CreateBlogPost.as_view(), name="create_blogpost_urlpattern"),
    path('blogpost/list/', ListBlogPosts.as_view(), name="list_blogpost_urlpattern"),
    path('blogpost/list/<int:user_id>', ListUserBlogPosts.as_view(), name="user_list_blogpost_urlpattern"),
    path('blogpost/update/<int:post_id>', UpdateBlogPost.as_view(), name="update_blogpost_urlpattern"),
    path('blogpost/delete/<int:post_id>', DeleteBlogPost.as_view(), name="delete_blogpost_urlpattern"),
    path('blogpost/search/<str:search_keyword>', SearchBlogPost.as_view(), name="search_blogpost_urlpattern"),
]
=======
    path('blogpost/create', CreateBlogPost.as_view(),
         name="create_blogpost_urlpattern"),
    path('blogpost/list/', ListBlogPosts.as_view(),
         name="list_blogpost_urlpattern"),
    path('blogpost/list/<int:user_id>', ListUserBlogPosts.as_view(),
         name="user_list_blogpost_urlpattern"),
    path('blogpost/update/<int:post_id>', UpdateBlogPost.as_view(),
         name="update_blogpost_urlpattern"),
    path('blogpost/delete/<int:post_id>', DeleteBlogPost.as_view(),
         name="delete_blogpost_urlpattern"),
    path('blogpost/search/<str:search_keyword>',
         SearchBlogPost.as_view(), name="search_blogpost_urlpattern"),
    path('blogpost/likepost', LikeBlogPost.as_view(),
         name="like_blogpost_urlpattern"),
    # path('travelinfo/create/<int:user_id>', CreateTravelInfo.as_view(),
    #      name="create_travelinfo_urlpattern"),
    path('travelinfo/update/<int:user_id>', UpdateTravelInfo.as_view(),
         name="update_travelinfo_urlpattern"),
    path('comment/create/<int:user_id>/<int:parent_id>/<int:post_id>', CreateComment.as_view(),
         name="create_comment_urlpattern"),
    path('comment/update/<int:user_id>/<int:comment_id>', UpdateComment.as_view(),
         name="update_comment_urlpattern"),

]
>>>>>>> Stashed changes
