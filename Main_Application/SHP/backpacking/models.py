# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Buser(models.Model):
    userid = models.AutoField(primary_key=True)
    open_match = models.IntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    profile_pic = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BUser'


class Blogphoto(models.Model):
    photoid = models.AutoField(primary_key=True)
    photo_url = models.CharField(max_length=100, blank=True, null=True)
    postid = models.ForeignKey('Blogpost', models.DO_NOTHING, db_column='postid')

    class Meta:
        managed = False
        db_table = 'BlogPhoto'


class Blogpost(models.Model):
    postid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=10000, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(Buser, models.DO_NOTHING, db_column='author', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BlogPost'


class Blogtag(models.Model):
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid', primary_key=True)
    tagid = models.ForeignKey('Tag', models.DO_NOTHING, db_column='tagid')

    class Meta:
        managed = False
        db_table = 'BlogTag'
        unique_together = (('postid', 'tagid'),)


class Comment(models.Model):
    commentid = models.AutoField(primary_key=True)
    comment_time = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid', blank=True, null=True)
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid')
    parentid = models.ForeignKey('self', models.DO_NOTHING, db_column='parentid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Comment'


class Likepost(models.Model):
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid', primary_key=True)
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid')

    class Meta:
        managed = False
        db_table = 'LikePost'
        unique_together = (('userid', 'postid'),)


class Tag(models.Model):
    tagid = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50, blank=True, null=True)
    tag_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tag'


class Travelinfo(models.Model):
    travelinfo_id = models.AutoField(primary_key=True)
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
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid', primary_key=True)
    tagid = models.ForeignKey(Tag, models.DO_NOTHING, db_column='tagid')

    class Meta:
        managed = False
        db_table = 'UserTag'
        unique_together = (('userid', 'tagid'),)
