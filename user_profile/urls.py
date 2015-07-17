from django.conf.urls import patterns, url

"""NOTE these urls are mounted in the main app under /accounts/ IN
ADDITION to the urls provided by django-allauth. Be very careful not
to overwrite an existing url when adding to this file.
"""
urlpatterns = patterns(
    '',
    url(r'^profile/$', 'user_profile.views.profile', name='profile'),
    url(r'^upload_avatar/$', 'user_profile.views.upload_avatar', name='avatar_form'),
)
