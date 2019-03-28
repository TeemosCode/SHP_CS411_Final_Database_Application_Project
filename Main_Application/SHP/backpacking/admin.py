from django.contrib import admin
from .models import Blogphoto, Blogpost, Blogtag, \
    Buser, Comment, Tag, Travelinfo, Likepost, Usertag

# Register your models here.
admin.site.register(Blogpost)
admin.site.register(Blogphoto)
admin.site.register(Blogtag)
admin.site.register(Buser)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Travelinfo)
admin.site.register(Likepost)
admin.site.register(Usertag)
