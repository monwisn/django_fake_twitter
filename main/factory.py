import factory
import faker
from django.contrib.auth.models import User

from .models import Book


FAKE = faker.Faker()


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=8)
    slug = factory.Faker('slug')
    genre = factory.Faker('sentence', nb_words=3)
    author = User.objects.get_or_create(username='admin')[0]
    isbn = factory.LazyAttribute(lambda x: faker.generator.random.randrange(1E+12, 1E+13))
