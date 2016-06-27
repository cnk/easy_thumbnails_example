import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    # Default values
    first_name = 'Some'
    last_name = 'User'
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.LazyAttribute(lambda obj: '{}@test.edu'.format(obj.username))
    password = make_password('password')
    is_active = True

