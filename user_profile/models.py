from django.db import models
from django.conf import settings
# register a signal to create a thumbnail from any new avatar images
# from easy_thumbnails.signals import saved_file  # noqa


class UserProfile(models.Model):
    """
    Provides a user-uploaded avatar image - or a default with the user's initials
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    avatar_height = models.PositiveIntegerField()
    avatar_width = models.PositiveIntegerField()
    avatar = models.ImageField(upload_to='avatars/',
                               height_field='avatar_height',
                               width_field='avatar_width',
                               max_length=512,
                               )

    def __str__(self):
        return self.user.username
