from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils.six import BytesIO
from .factories import UserFactory
from .models import UserProfile


# "borrowed" from easy_thumbnails/tests/test_processors.py
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class UserTests(TestCase):
    def setUp(self):
        self.user = UserFactory(username='me')

    def tearDown(self):
        self.user.delete()

    def test_adding_an_avatar_image(self):
        # make sure we start out with no UserProfile (and thus no avatar)
        self.assertIsNone(UserProfile.objects.filter(user_id=self.user.id).first())
        myClient = Client()
        myClient.login(username=self.user.username, password='password')

        # set up form data
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        form_data = {'avatar': avatar}

        response = myClient.post(reverse('avatar_form'), form_data, follow=True)
        self.assertRegex(response.redirect_chain[0][0], r'/users/profile/$')
        # And now there is a user profile with an avatar
        self.assertIsNotNone(self.user.profile.avatar)

    def test_uploading_non_image_file_errors(self):
        # make sure we start out with no UserProfile (and thus no avatar)
        self.assertIsNone(UserProfile.objects.filter(user_id=self.user.id).first())
        myClient = Client()
        myClient.login(username=self.user.username, password='password')

        # set up form data
        text_file = SimpleUploadedFile('front.png', b'this is some text - not an image')
        form_data = {'avatar': text_file}

        response = myClient.post(reverse('avatar_form'), form_data, follow=True)
        self.assertFormError(response, 'avatar_form', 'avatar', 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')

