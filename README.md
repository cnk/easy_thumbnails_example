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

To run this example, clone the repository and checkout the 'round-1'
tag. Then set up to run the development server:

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



## Round 2: Clean up

Checkout the 'round-2' tag and 'pip install -r requirements.txt'.

To remove files that have been replaced / superceded, I added
django-cleanup. Checkout the 'round-2' tag and 'pip install -r
requirements.txt'.

Now when you upload a new image to replace your current avatar, the
old file gets removed, leaving only the new image. Well actually
django-cleanup only removes the file mentioned in the database table
for the user profile. To get rid of the rest of the cruft from round
1, you will need to delete the files yourself.

Next, most sites want to create thumbnails of their images for one
reason or another. Let's do that using easy-thumbnails - in round 3:

    git checkout -b 'round-3'



## Round 3: Creating thumbnails

Checkout the 'round-3' tag and 'pip install -r requirements.txt' to
install easy-thumbnails:
https://github.com/SmileyChris/easy-thumbnails. Run the migrations and
then start the server again.

This round added configuration options (and database tables) for
creating thumbnails to be created on the fly whenever they are
requested. The generaged thumbnails are stored for the next time they
are created. When using the file system, the images will be stored
whereever THUMBNAIL_BASEDIR says. By default that will be where ever
your ImageField is storing the originals.

So upload a couple of different avatars to try them out - then look in
the 'media/avatars/' folder. Notice that django-cleanup is still
removing the obsoleted originals - but is not deleting the
corresponding thumbnails. So once again we are accumulating cruft. I
am not the first person to report this; but the ticket on the
django-cleanup project -
https://github.com/un1t/django-cleanup/issues/14 - says this should
just work. Hmmm. I wonder what changed.




## Round 4: Cleaning up thumbnails

Checkout the 'round-4' tag, run the migrations, and then start the
server again.

The django-cleaner maintainer pointed me to the test suite which is
still passing. Looking at the tests, the main difference I see is that
they are using `easy_thumbnails.fields.ThumbnailerImageField` while I
have been using the stock Django `django.db.models.ImageField`. Sure
enough, after I changed the field type, uploading a new avatar
replaces the previous image AND it's thumbnail.




## Round 5: Storing images in S3

Checkout the 'round-5' tag and 'pip install -r requirements.txt' to
install django-storages-redux and boto (a library for interacting with
AWS S3). In order to make this example work, you will need to set up
an S3 bucket and put the AWS credentials into the settings.py file.

The instructions in this blog post,
https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/,
are very useful for setting up your S3 bucket. Some of the rest of the
information is good, but there are a few more configuration options
now, so separating the static file and media storage options is
easier.  This example contains the minimal configuration for moving
media files into S3 while leaving the static files in the file system.

Restart your server and upload a new avatar. Note that the url for
your thumbnail is now on the server defined by the
AWS_S3_CUSTOM_DOMAIN parameter.




## Round 6: How to upload an image in a form + view test

Checkout the 'round-6' tag. I don't want to have to depend on S3 when
I am noodling around on my laptop, so the first commit in this round
reverses the S3 storage configuration changes from round 5.

