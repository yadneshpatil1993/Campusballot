# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(unique=True, max_length=50)),
                ('org_name', models.CharField(max_length=50)),
                ('male_count', models.IntegerField(default=0)),
                ('female_count', models.IntegerField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('u_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupQn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.ForeignKey(to='group.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('gender', models.CharField(default=False, max_length=1, choices=[(b'0', b'Female'), (b'1', b'Male')])),
                ('group_id', models.ForeignKey(to='group.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200)),
                ('gender', models.CharField(default=False, max_length=1, choices=[(b'0', b'All'), (b'1', b'Female'), (b'2', b'Male')])),
                ('is_groupspecifc', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('member_id', models.ForeignKey(to='group.Members')),
                ('question', models.ForeignKey(to='group.Questions')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suggested_members',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('suggestion', models.CharField(max_length=50)),
                ('gender', models.CharField(default=False, max_length=1, choices=[(b'0', b'Female'), (b'1', b'Male')])),
                ('group_id', models.ForeignKey(to='group.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suggested_questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('suggestion', models.CharField(max_length=50)),
                ('gender', models.CharField(default=False, max_length=1, choices=[(b'0', b'All'), (b'1', b'Female'), (b'2', b'Male')])),
                ('is_accepted', models.BooleanField(default=False)),
                ('group_id', models.ForeignKey(to='group.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='groupqn',
            name='qn_id',
            field=models.ForeignKey(to='group.Questions'),
            preserve_default=True,
        ),
    ]
