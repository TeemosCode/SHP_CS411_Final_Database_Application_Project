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
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    profile_pic = models.CharField(max_length=200, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    info = models.CharField(max_length=10000, blank=True, null=True)
    facebook_user_id = models.CharField(unique=True, max_length=128, blank=True, null=True)

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
    create_time = models.DateTimeField()
    author = models.ForeignKey(Buser, models.DO_NOTHING, db_column='author', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BlogPost'


class Blogtag(models.Model):
    blogtagid = models.AutoField(primary_key=True)
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid')
    tag = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'BlogTag'


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
    likeid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(Buser, models.DO_NOTHING, db_column='userid')
    postid = models.ForeignKey(Blogpost, models.DO_NOTHING, db_column='postid')

    class Meta:
        managed = False
        db_table = 'LikePost'


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
