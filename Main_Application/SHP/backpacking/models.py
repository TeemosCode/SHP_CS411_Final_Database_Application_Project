# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Buser(models.Model):
    userid = models.IntegerField(primary_key=True)
    open_match = models.IntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    profile_pic = models.CharField(max_length=200, blank=True, null=True)
    travelinfo_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BUser'


class Bloghasphoto(models.Model):
    postid = models.ForeignKey('Blogpost', models.DO_NOTHING, db_column='postid')
    photoid = models.ForeignKey('Blogphoto', models.DO_NOTHING, db_column='photoid')

    class Meta:
        managed = False
        db_table = 'BlogHasPhoto'


class Blogphoto(models.Model):
    photoid = models.IntegerField(primary_key=True)
    photo_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BlogPhoto'


class Blogpost(models.Model):
    postid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=10000, blank=True, null=True)
    author = models.ForeignKey(Buser, models.DO_NOTHING, db_column='author', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BlogPost'


class Blogtag(models.Model):
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid')
    tagid = models.ForeignKey('Tag', models.DO_NOTHING, db_column='tagid')

    class Meta:
        managed = False
        db_table = 'BlogTag'


class Comment(models.Model):
    commentid = models.IntegerField(primary_key=True)
    comment_time = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid')
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'Comment'


class Likepost(models.Model):
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid')
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid')

    class Meta:
        managed = False
        db_table = 'LikePost'


class Reply(models.Model):
    parentid = models.ForeignKey(Comment, models.DO_NOTHING, db_column='parentid')
    commentid = models.ForeignKey(Comment, models.DO_NOTHING, db_column='commentid')

    class Meta:
        managed = False
        db_table = 'Reply'


class Tag(models.Model):
    tagid = models.IntegerField(primary_key=True)
    tag_name = models.CharField(max_length=50, blank=True, null=True)
    tag_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tag'


class Travelinfo(models.Model):
    travelinfo_id = models.IntegerField(primary_key=True)
    activity = models.CharField(max_length=200, blank=True, null=True)
    budgetmax = models.IntegerField(db_column='budgetMax', blank=True, null=True)  # Field name made lowercase.
    budgetmin = models.IntegerField(db_column='budgetMin', blank=True, null=True)  # Field name made lowercase.
    destination = models.CharField(max_length=100, blank=True, null=True)
    starttime = models.DateField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Travelinfo'


class Usertag(models.Model):
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid')
    tagid = models.ForeignKey(Tag, models.DO_NOTHING, db_column='tagid')

    class Meta:
        managed = False
        db_table = 'UserTag'
