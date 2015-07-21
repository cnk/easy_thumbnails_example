from django.db import models
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField

class UserProfile(models.Model):
    """
    Provides a user-uploaded avatar image.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    avatar_height = models.PositiveIntegerField()
    avatar_width = models.PositiveIntegerField()
    avatar = ThumbnailerImageField(upload_to='avatars/',
                                   height_field='avatar_height',
                                   width_field='avatar_width',
                                   max_length=512,
                                  )

    def __str__(self):
        return self.user.username
