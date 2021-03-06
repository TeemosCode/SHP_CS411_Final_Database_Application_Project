# Generated by Django 2.1.7 on 2019-03-30 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogphoto',
            fields=[
                ('photoid', models.AutoField(primary_key=True, serialize=False)),
                ('photo_url', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'BlogPhoto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('postid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=10000, null=True)),
            ],
            options={
                'db_table': 'BlogPost',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Buser',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('open_match', models.IntegerField(blank=True, null=True)),
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('info', models.CharField(blank=True, max_length=500, null=True)),
                ('profile_pic', models.CharField(blank=True, max_length=200, null=True)),
                ('travelinfo_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'BUser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentid', models.AutoField(primary_key=True, serialize=False)),
                ('comment_time', models.DateTimeField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=5000, null=True)),
            ],
            options={
                'db_table': 'Comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagid', models.AutoField(primary_key=True, serialize=False)),
                ('tag_name', models.CharField(blank=True, max_length=50, null=True)),
                ('tag_type', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Tag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Travelinfo',
            fields=[
                ('travelinfo_id', models.AutoField(primary_key=True, serialize=False)),
                ('activity', models.CharField(blank=True, max_length=200, null=True)),
                ('budgetmax', models.IntegerField(blank=True, db_column='budgetMax', null=True)),
                ('budgetmin', models.IntegerField(blank=True, db_column='budgetMin', null=True)),
                ('destination', models.CharField(blank=True, max_length=100, null=True)),
                ('starttime', models.DateField(blank=True, db_column='startTime', null=True)),
                ('endtime', models.DateField(blank=True, db_column='endTime', null=True)),
            ],
            options={
                'db_table': 'Travelinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Blogtag',
            fields=[
                ('postid', models.ForeignKey(db_column='postid', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='backpacking.Blogpost')),
            ],
            options={
                'db_table': 'BlogTag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Likepost',
            fields=[
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='backpacking.Buser')),
            ],
            options={
                'db_table': 'LikePost',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usertag',
            fields=[
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='backpacking.Buser')),
            ],
            options={
                'db_table': 'UserTag',
                'managed': False,
            },
        ),
    ]
