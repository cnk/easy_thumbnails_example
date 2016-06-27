from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^profile/$', 'user_profile.views.profile', name='profile'),
    url(r'^upload_avatar/$', 'user_profile.views.upload_avatar', name='avatar_form'),
)
