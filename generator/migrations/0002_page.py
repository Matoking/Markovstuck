# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-10 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('image', models.IntegerField()),
                ('pre_dialog_text', models.TextField()),
                ('dialoglog_text', models.TextField()),
                ('post_dialog_text', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('saved', models.BooleanField(default=False)),
            ],
        ),
    ]
