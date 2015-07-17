# User Avatar Example

Example of how to combine django's ImageField to upload images and
easy-thumbnails to create thumbnails.

Django's ImageField does not delete old images when they are replaced
with new ones. So I added django-cleanup to take care of this. This
does take care of removing the old originals but NOT the cached
thumbnails - despite this ticket indicating that it should:
https://github.com/un1t/django-cleanup/issues/14

## Round 1: Basic image upload to the file system

Generic site with a user_profile model that adds an avatar to each
user. The avatar upload uses Django's built in ImageField

For this iteration I am not doing any thumbnailing and the images are
just uploaded to a subdirectory of MEDIA_ROOT.

NOTE: To be able to see the media files when using `./manage.py
runserver` you need to configure a MEDIA_URL and MEDIA_ROOT and then
add a section to your main urls.py that asks the dev server to serve
these static files:

    ## in your settings.py
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.8/howto/static-files/

    STATIC_URL = '/static/'

    MEDIA_URL = '/files/'
    MEDIA_ROOT = BASE_DIR + '/media'


    # in your site's urls.py
    if settings.DEBUG:
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        from django.conf.urls.static import static
        urlpatterns += staticfiles_urlpatterns()
        # and for media files
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

To run this example, clone the repository and set up to run the
development server:

    git clone https://github.com/cnk/easy_thumbnails_example.git
    git checkout -b round-1
    ## however you create your virtual environments
    pip install -r requirements.txt
    # You may need to install some libraries for installing Pillow
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

Go to the hompage, click the link and log in using the admin
credentials you created above. Upload an image. You will see the file
in the 'media/avatars/' directory. Now upload a new image. The new
image will be displayed on the profile page - but the new and old
images are both in 'media/avatars/'. If you uploaded the same image a
second time, you will see the second image has been uploaded with a
'random' string appended to make a unique file name.

We should not be accumulating this sort of cruft. To see how to fix this:

    git checkout -b 'round-2'
