from django.contrib import admin

# Register your models here.
from .models import Buser, Blogphoto, Blogpost, Blogtag, Comment, Likepost, Travelinfo

admin.site.register(Buser)
admin.site.register(Blogphoto)
admin.site.register(Blogpost)
admin.site.register(Blogtag)
admin.site.register(Comment)
admin.site.register(Likepost)
admin.site.register(Travelinfo)
