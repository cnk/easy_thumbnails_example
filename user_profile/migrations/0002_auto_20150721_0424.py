# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(height_field='avatar_height', max_length=512, upload_to='avatars/', width_field='avatar_width'),
        ),
    ]
