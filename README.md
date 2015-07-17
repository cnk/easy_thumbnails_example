## Example site

Example of how to combine django's ImageField to upload images and
easy-thumbnails to create thumbnails.

Django's ImageField does not delete old images when they are replaced
with new ones. So I added django-cleanup to take care of this. This
does take care of removing the old originals but NOT the cached
thumbnails - despite this ticket indicating that it should:
https://github.com/un1t/django-cleanup/issues/14